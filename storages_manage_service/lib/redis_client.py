from json import dumps
from redis import Redis

# Redis documentation - https://redis.io/docs/clients/python/
Red = Redis(host='localhost', port=6379, decode_responses=True)

# test demo how it works
if __name__ == '__main__':
    # put dict in redis under key "test-key"
    Red.hset('test-key', mapping={"a": 1, "b": 2})
    # get it by key
    print(Red.hgetall('test-key'))
    # primitive way. Code to json, put as json string
    Red.set('test-2', dumps({1: 2, 3: 4}))
    # get this string. decode_responses = True, so it will be decoded to python dict
    print(Red.get('test-2'))
