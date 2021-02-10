import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from .config import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE

from sqlalchemy.sql.schema import RETAIN_SCHEMA


## Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_jwt_auth_header():
    authorization = request.headers.get('Authorization', None)

    if not authorization:
        raise AuthError({
            'code': 401,
            'description': 'Authorization header is expected'
        }, 401)

    splited_auth_header = authorization.split(' ')
    jwt = ''
    if splited_auth_header[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header is misconfigured'
        }, 401)

    elif len(splited_auth_header) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(splited_auth_header) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)   
    
    jwt = splited_auth_header[1]
    if not jwt or jwt == 'null':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'No token was found'
        }, 401)

    return jwt


def verify_and_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    
    
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)
    
    rsa_key = {}
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
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

def check_the_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
                'code': 'invalid_permissions',
                'description': 'check your RBAC settings in Auth0'
            }, 401)
    
    if permission not in payload['permissions']:
        raise AuthError({
                'code': 'insufficient_permission',
                'description': 'You don\'t have access to the requested resource.'
            }, 403)
    
    return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_jwt_auth_header()
            payload = verify_and_decode_jwt(token)
            check_the_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator