import os
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, redirect, render_template, url_for, request, _request_ctx_stack, abort
from six.moves.urllib.parse import urlencode
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.environ.get('AUTH_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
CLIENT_ID = os.environ.get('CLIENT_ID')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

def build_login_link():
    link = "https://"
    link += AUTH0_DOMAIN + "/authorize?audience="
    link += API_AUDIENCE + "&scope="
    link += "openid profile email" + "&response_type=token&client_id="
    link += CLIENT_ID + "&redirect_uri="
    link += REDIRECT_URI

    return link


"""
def setup_auth(app):
    oauth = OAuth(app)
    app.secret_key = 'hello'

    auth0 = oauth.register(
    'auth0',
    client_id='jwO5atsdz0jn3bKDp7Ip4j22RhPG7w9q',
    client_secret='oExvWpyMKezbp1a5PVX00GEXBVVmtpGmY-aOkjKmMXZeIK9CuSq5EmfvubKq2-LY',
    api_base_url='https://dev-jyqum17r.auth0.com',
    access_token_url='https://dev-jyqum17r.auth0.com/oauth/token',
    authorize_url='https://dev-jyqum17r.auth0.com/authorize',
    #response_type="token"
    audience='warranty',
    client_kwargs={
        'scope': 'openid profile email',
         },
    )
    
    return auth0
"""


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    # Get header from request
    auth_header = request.headers.get('Authorization', None)
    token = None

    if auth_header is None:
        raise AuthError({
            'code': 401,
            'description': 'No authorization header found'
        }, 401)

    else:
        # header is present
        # Split the bearer and token
        auth_header_parts = auth_header.split()

        # Check if header is malformed
        if len(auth_header_parts) != 2:

            raise AuthError({
                'code': 401,
                'description': 'Header is malformed'
            }, 401)

        if auth_header_parts[0].lower() != 'bearer':

            raise AuthError({
                'code': 401,
                'description': 'Header token is not of type Bearer'
            }, 401)

        token = auth_header_parts[1]

    return token

def check_permissions(permission, payload):
    # Check if permission is in payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 401,
            'message': 'No permissions in the payload'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 401,
            'message': 'No permissions in the payload'
        }, 401)

    return True

def verify_decode_jwt(token):
    # Check for key id (kid)
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 401,
            'description': 'No key ID: authorization is malformed'
        }, 401)

    # Verify the token using Auth0 /.well-known/jwks.json
    domain_url = 'https://%s/.well-known/jwks.json' % (AUTH0_DOMAIN)
    jsonurl = urlopen(domain_url)
    content = jsonurl.read().decode(jsonurl.headers.get_content_charset())
    jwks = json.loads(content)
    rsa_key = {}

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience\
                                and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
