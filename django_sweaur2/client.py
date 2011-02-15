from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from sweaur2.client import Client as Sweaur2Client
from sweaur2.client_store import ClientStore


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
