from __future__ import absolute_import

import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from sweaur2.exceptions import InvalidCredentials, OAuth2Error, InvalidRequest
from sweaur2.processor import OAuth2Processor

from .client import DjangoClientStore
from .models import DjangoTokenStore


def import_policy():
    policy = getattr(settings, 'DJANGO_SWEAUR2_POLICY',
                     'django_sweaur2.policy.DjangoDefaultPolicy')
    if isinstance(policy, basestring):
        try:
            module, cls = policy.rsplit('.', 1)
        except ValueError:
            raise ValueError("Couldn't parse DJANGO_SWEAUR2_POLICY")
        policy = getattr(__import__(module, globals(), locals(), [cls]), cls)
        if isinstance(policy, type):
            policy = policy()
    return policy


class OAuth2TokenEndpoint(object):
    def __init__(self):
        self.processor = OAuth2Processor(
            client_store=DjangoClientStore(),
            token_store=DjangoTokenStore(),
            policy=import_policy()
            )

    @staticmethod
    def normalize_params(queryparams):
        # Drop all params with no value, and stringify keys
        # so we can ** them below
        params = {}
        for k in queryparams:
            v = queryparams.getlist(k)
            if not v:
                continue
            if len(v) != 1:
                raise InvalidRequest("Multiple values for '%s'" % k)
            params[str(k)] = v[0]
        return params

    csrf_exempt = True
    def __call__(self, req):
        if not req.is_secure() and not settings.DEBUG:
            return HttpResponseBadRequest()
        if not req.method == 'POST':
            return HttpResponseNotAllowed(['POST'])
        try:
            params = self.normalize_params(req.POST)
            access_token = self.processor.oauth2_token_endpoint(**params)
        except InvalidCredentials, e:
            resp = HttpResponse()
            resp.status_code = 401
            resp['WWW-Authenticate'] = e.www_authenticate
        except OAuth2Error, e:
            resp = HttpResponseBadRequest(json.dumps(e.as_dict()),
                                           mimetype='application/json')
        except Exception, e:
            raise
        else:
            resp = HttpResponse(json.dumps(access_token.as_dict()),
                                mimetype='application/json')
            resp['Cache-Control'] = 'no-store'
        return resp


token_endpoint = OAuth2TokenEndpoint()
