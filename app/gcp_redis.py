import redis
import os

KEY_TIME_TO_EXPIRE = 300 # seconds

def redis_client():
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_contact(contact_id):
    contact = redis_client().hgetall(contact_id)
    return contact


def set_contact(contact):
    redis_client().hmset(contact['id'], contact)
    redis_client().expire(contact['id'], KEY_TIME_TO_EXPIRE)
