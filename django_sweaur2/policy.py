from __future__ import absolute_import

from sweaur2.policy import DefaultPolicy
from sweaur2.token_types import token_type_map

from .models import AccessToken, RefreshToken


class DjangoDefaultPolicy(DefaultPolicy):
    def new_access_token_string(self, client, scope):
        while True:
            new_token_string = super(DjangoDefaultPolicy, self).new_access_token_string(client, scope)
            if not AccessToken.objects.filter(token_string=new_token_string).exists():
                 break
        return new_token_string

    def new_refresh_token_string(self, client, scope):
        while True:
            new_token_string = super(DjangoDefaultPolicy, self).new_refresh_token_string(client, scope)
            if not RefreshToken.objects.filter(token_string=new_token_string).exists():
                 break
        return new_token_string
