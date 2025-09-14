
import redis, os, time
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
_redis = None
def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(REDIS_URL)
    return _redis

class UserLock:
    def __init__(self, user_id, timeout=30):
        self.user_id = user_id
        self.key = f"user_lock:{user_id}"
        self.timeout = timeout
        self.redis = get_redis()
        self.token = str(time.time())

    def acquire(self):
        return self.redis.set(self.key, self.token, nx=True, ex=self.timeout)

    def release(self):
        val = self.redis.get(self.key)
        try:
            if val and val.decode() == self.token:
                self.redis.delete(self.key)
                return True
        except Exception:
            pass
        return False

    def __enter__(self):
        acquired = False
        start = time.time()
        while not acquired and (time.time() - start) < self.timeout:
            acquired = self.acquire()
            if not acquired:
                time.sleep(0.1)
        if not acquired:
            raise Exception('Could not acquire user lock')
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.release()
        except Exception:
            pass
