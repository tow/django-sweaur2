from __future__ import absolute_import

import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models

from sweaur2.client import Client as Sweaur2Client
from sweaur2.client_store import ClientStore
from sweaur2.token_store import TokenStore
from sweaur2.tokens import AccessToken as Sweaur2AccessToken, RefreshToken as Sweaur2RefreshToken

from .settings import ACCESS_TOKEN_LENGTH, ACCESS_TOKEN_SECRET_LENGTH


class TokenManager(models.Manager):
    def create_from_sweaur2_token(self, token):
        return self.create(client=token.client.user, 
                          token_string=token.token_string,
                          expires_in=token.expires_in)


class Token(models.Model):
    client = models.ForeignKey(User)
    token_string = models.CharField(max_length=ACCESS_TOKEN_LENGTH, unique=True)
    creation_time = models.DateTimeField()
    expires_in = models.IntegerField(null=True)

    class Meta(object):
        abstract = True

    objects = TokenManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_time = datetime.datetime.now()
        super(Token, self).save(*args, **kwargs)

    def to_sweaur2_token(self):
        if isinstance(self, AccessToken):
            return AccessToken()
        elif isinstance(self, RefreshToken):
            return RefreshToken()


class RefreshToken(Token):
    class Meta(object):
        abstract = True


class AccessToken(Token):
    class Meta(object):
        abstract = True


class BearerRefreshToken(RefreshToken):
    pass
class BearerAccessToken(AccessToken):
    old_refresh_token = models.OneToOneField(BearerRefreshToken, null=True, related_name='new_access_token')
    new_refresh_token = models.OneToOneField(BearerRefreshToken, null=True, related_name='old_access_token')


class MACRefreshToken(RefreshToken):
    pass
class MACAccessToken(AccessToken):
    old_refresh_token = models.OneToOneField(MACRefreshToken, null=True, related_name='new_access_token')
    new_refresh_token = models.OneToOneField(MACRefreshToken, null=True, related_name='old_access_token')

    secret_token_string = models.CharField(max_length=ACCESS_TOKEN_SECRET_LENGTH)
    algorithm = models.SmallIntegerField()   


access_token_type_map = {
   'Bearer':BearerAccessToken,
   'MAC':MACAccessToken,
}
refresh_token_type_map = {
   'Bearer':BearerRefreshToken,
   'MAC':MACRefreshToken,
}

class DjangoTokenStore(TokenStore):
    def save_access_token(self, token):
        try:
            token_impl = access_token_type_map[token.token_type]
        except KeyError:
            raise ValueError("Unknown token type")
        try:
            db_token_obj = token_impl.objects.get(token_string=token.token_string)
            db_token_obj.update(token)
        except token_impl.DoesNotExist:
            token_impl.objects.create_from_sweaur2_token(token)

    def save_refresh_token(self, token):
        try:
            token_impl = access_token_type_map[token.token_type]
        except KeyError:
            raise ValueError("Unknown token type")
        try:
            db_token_obj = token_impl.objects.get(token_string=token.token_string)
            db_token_obj.update(token)
        except token_impl.DoesNotExist:
            token_impl.objects.create_from_sweaur2_token(token)

    def get_access_token(self, token_type, token_string):
        try:
            token_impl = access_token_type_map[token.token_type]
        except KeyError:
            raise ValueError("Unknown token type")  
        try:
            return token_impl.objects.get(token_string=token_string).to_sweaur2_token()
        except token_impl.DoesNotExist:
            raise self.NoSuchToken()

    def get_refresh_token(self, token_type, token_string):
        try:
            token_impl = refresh_token_type_map[token.token_type]
        except KeyError:
            raise ValueError("Unknown token type")  
        try:
            return token_class.objects.get(token_string=token_string).to_sweaur2_token()
        except token_impl.DoesNotExist:
            raise self.NoSuchToken()


class Client(Sweaur2Client):
    def __init__(self, user):
        self.user = user
        self.client_id = user.username

    def check_secret(self, client_secret):
        user = authenticate(self.client_id, client_secret)
        if user:
            return user.is_active
        return False

    def delete(self):
        self.user.delete()


class DjangoClientStore(ClientStore):
    def make_client(self, client_id, client_secret, active=True):
        user = User.objects.create(username=client_id)
        user.set_password(client_secret)
        if not active:
            user.is_active = False
        user.save()
        return Client(user)

    def get_client(self, client_id):
        try:
            return Client(User.objects.get(username=client_id))
        except User.DoesNotExist:
            raise self.NoSuchClient()
