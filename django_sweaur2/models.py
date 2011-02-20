from __future__ import absolute_import

import datetime, json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import get_cache
from django.core.cache.backends.dummy import DummyCache
from django.db import models

from sweaur2.token_store import TokenStore
from sweaur2.tokens import AccessToken as Sweaur2AccessToken, RefreshToken as Sweaur2RefreshToken

from .client import Client
from .settings import ACCESS_TOKEN_LENGTH, ACCESS_TOKEN_SECRET_LENGTH, CACHE_FOR_NONCE, CACHE_PREFIX_FOR_NONCE, CACHE_TIMEOUT_FOR_NONCE


class DjangoTokenStore(models.Manager, TokenStore):
    token_types = (
        'bearer',
        'mac',
    )

    def __init__(self, *args, **kwargs):
        try:
            self.cache = get_cache(CACHE_FOR_NONCE)
        except KeyError:
            raise EnvironmentError("Must configure cache for django-sweaur2")
        if isinstance(self.cache, DummyCache) and not settings.DEBUG:
            raise EnvironmentError("Don't use the DummyCache for django-sweaur2")
        super(DjangoTokenStore, self).__init__(*args, **kwargs)

    def create_from_sweaur2_access_token(self, token):
        return self.create(client=token.client.user, 
                           token_string=token.token_string,
                           scope=token.scope,
                           token_type_id=self.token_types.index(token.token_type),
                           expires_in=token.expires_in,
                           extra_parameters=json.dumps(token.extra_parameters))

    def create_from_sweaur2_refresh_token(self, token):
        return self.create(client=token.client.user, 
                           token_string=token.token_string,
                           scope=token.scope)

    def save_access_token(self, token):
        try:
            db_token_obj = AccessToken.objects.get(token_string=token.token_string)
        except AccessToken.DoesNotExist:
            db_token_obj = AccessToken.objects.create_from_sweaur2_access_token(token)
        if token.old_refresh_token_string:
            db_token_obj.old_refresh_token = RefreshToken.objects.get(token_string=token.old_refresh_token_string)
        if token.new_refresh_token_string:
            db_token_obj.new_refresh_token = RefreshToken.objects.get(token_string=token.new_refresh_token_string)
        db_token_obj.save()

    def save_refresh_token(self, token):
        try:
            db_token_obj = RefreshToken.objects.get(token_string=token.token_string)
        except RefreshToken.DoesNotExist:
            db_token_obj = RefreshToken.objects.create_from_sweaur2_refresh_token(token)

    def get_access_token(self, token_string, token_type):
        try:
            token_type_id = self.token_types.index(token_type)
        except ValueError:
            raise ValueError("Unknown token_type")
        try:
            return AccessToken.objects.get(token_string=token_string, token_type_id=token_type_id).to_sweaur2_token()
        except AccessToken.DoesNotExist:
            raise self.NoSuchToken()

    def get_refresh_token(self, token_string):
        try:
            return RefreshToken.objects.get(token_string=token_string).to_sweaur2_token()
        except RefreshToken.DoesNotExist:
            raise self.NoSuchToken()

    def check_nonce(self, nonce, timestamp, access_token):
        cache_label = '%s-%s-%s-%s' % (CACHE_PREFIX_FOR_NONCE, nonce, timestamp, access_token)
        if self.cache.get(cache_label):
            return False
        self.cache.set(cache_label, True, CACHE_TIMEOUT_FOR_NONCE)
        return True


class Token(models.Model):
    client = models.ForeignKey(User)
    token_string = models.CharField(max_length=ACCESS_TOKEN_LENGTH, unique=True)
    scope = models.TextField(blank=True, null=True)
    creation_time = models.DateTimeField()

    class Meta(object):
        abstract = True

    objects = DjangoTokenStore()

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_time = datetime.datetime.now()
        super(Token, self).save(*args, **kwargs)


class RefreshToken(Token):
    def to_sweaur2_token(self):
        try:
            old_access_token_string = self.old_access_token.token_string
        except AccessToken.DoesNotExist:
            old_access_token_string = None
        try:
            new_access_token_string = self.new_access_token.token_string
        except AccessToken.DoesNotExist:
            new_access_token_string = None
        return Sweaur2RefreshToken(client=Client(self.client),
                                   scope=self.scope,
                                   old_access_token_string=old_access_token_string,
                                   new_access_token_string=new_access_token_string,
                                   token_string=self.token_string)


class AccessToken(Token):
    expires_in = models.IntegerField(null=True)
    old_refresh_token = models.OneToOneField(RefreshToken, null=True, related_name='new_access_token')
    new_refresh_token = models.OneToOneField(RefreshToken, null=True, related_name='old_access_token')
    token_type_id = models.SmallIntegerField()
    extra_parameters = models.TextField(blank=True)

    def to_sweaur2_token(self):
        if self.old_refresh_token:
            old_refresh_token_string = self.old_refresh_token.token_string
        else:
            old_refresh_token_string = None
        if self.new_refresh_token:
            new_refresh_token_string = self.new_refresh_token.token_string
        else:
            new_refresh_token_string = None
        return Sweaur2AccessToken(client=Client(self.client),
                                  scope=self.scope,
                                  token_type=DjangoTokenStore.token_types[self.token_type_id],
                                  expires_in=self.expires_in,
                                  token_string=self.token_string,
                                  old_refresh_token_string=old_refresh_token_string,
                                  new_refresh_token_string=new_refresh_token_string,
                                  **json.loads(self.extra_parameters))
