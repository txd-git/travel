import time
import jwt
from django.conf import settings



# 生成token
def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username': username, 'exp': now + expire}
    return jwt.encode(payload, key, algorithm='HS256')
