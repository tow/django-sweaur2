from __future__ import absolute_import

import datetime, json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models

from sweaur2.client import Client as Sweaur2Client
from sweaur2.client_store import ClientStore
from sweaur2.token_store import TokenStore
from sweaur2.tokens import AccessToken as Sweaur2AccessToken, RefreshToken as Sweaur2RefreshToken

from .settings import ACCESS_TOKEN_LENGTH, ACCESS_TOKEN_SECRET_LENGTH


class DjangoTokenStore(models.Manager, TokenStore):
    token_types = (
        'Bearer',
        'MAC',
    )

    def create_from_sweaur2_access_token(self, token):
        if token.token_type == 'Bearer':
            extra_parameters = {}
        if token.token_type == 'MAC':
            extra_parameters = {'secret_token_string':token.secret_token_string,
                                'algorithm':token.algorithm}
        return self.create(client=token.client.user, 
                           token_string=token.token_string,
                           scope=token.scope,
                           token_type_id=self.token_types.index(token.token_type),
                           expires_in=token.expires_in,
                           extra_parameters=extra_parameters)

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

    def get_access_token(self, token_string):
        try:
            return AccessToken.objects.get(token_string=token_string).to_sweaur2_token()
        except AccessToken.DoesNotExist:
            raise self.NoSuchToken()

    def get_refresh_token(self, token_string):
        try:
            return RefreshToken.objects.get(token_string=token_string).to_sweaur2_token()
        except RefreshToken.DoesNotExist:
            raise self.NoSuchToken()



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
        try:
            old_refresh_token_string = self.old_refresh_token.token_string
        except RefreshToken.DoesNotExist:
            old_refresh_token_string = None
        try:
            new_refresh_token_string = self.new_refresh_token.token_string
        except RefreshToken.DoesNotExist:
            new_refresh_token_string = None
        return Sweaur2AccessToken(client=Client(self.client),
                                  scope=self.scope,
                                  token_type=self.objects.token_types[self.token_type_id],
                                  expires_in=self.expires_in,
                                  token_string=self.token_string,
                                  old_refresh_token=old_refresh_token_string,
                                  new_refresh_token=new_refresh_token_string,
                                  extra_parameters=self.extra_parameters)


class Client(Sweaur2Client):
    def __init__(self, user):
        self.user = user
        self.client_id = user.username

    def check_secret(self, client_secret):
        user = authenticate(username=self.client_id, password=client_secret)
        if user:
            return user.is_active
        return False


class DjangoClientStore(ClientStore):
    def make_client(self, client, active=True):
        user = User.objects.create(username=client.client_id)
        user.set_password(client.client_secret)
        if not active:
            user.is_active = False
        user.save()
        return Client(user)

    def get_client(self, client_id, client_secret):
        try:
            client = Client(User.objects.get(username=client_id))
        except User.DoesNotExist:
            raise self.NoSuchClient()
        if not client.check_secret(client_secret):
            raise self.NoSuchClient()
        return client

    def delete_client(self, client):
        User.objects.get(username=client.client_id).delete()
