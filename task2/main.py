import redis
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, R, redis_host='localhost', redis_port=6379, redis_db=0):
        self.R = R
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
    
    def is_request_allowed(self, timestamp):
        current_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        current_timestamp = int(current_time.timestamp())
        
        self.redis_client.zremrangebyscore('requests', '-inf', current_timestamp - 3600)
        
        num_requests = self.redis_client.zcard('requests')
        
        if num_requests < self.R:
            self.redis_client.zadd('requests', {current_timestamp: current_timestamp})
            return True
        else:
            return False

def rate_limit_core(N, R, timestamps):
    rate_limiter = RateLimiter(R)
    result = []

    for timestamp in timestamps:
        is_allowed = rate_limiter.is_request_allowed(timestamp)
        result.append(is_allowed)

    return result

# Example usage
if __name__ == "__main__":
    N, R = map(int, input().split())
    timestamps = [input() for _ in range(N)]
    output = rate_limit_core(N, R, timestamps)
    for value in output:
        print(value)
