from __future__ import absolute_import

from sweaur2.constructor_tests import constructor_for_bearer_checks, constructor_for_token_endpoint

from .client import DjangoClientStore
from .models import DjangoTokenStore

globals().update(constructor_for_token_endpoint(DjangoTokenStore(), DjangoClientStore()))
globals().update(constructor_for_bearer_checks(DjangoTokenStore(), DjangoClientStore()))
