import redis

try:
    r = redis.Redis(host="redis", port=6379, db=0)
except Exception as e:
    print("Redis connection failed: ", e)

