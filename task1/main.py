from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, R):
        self.R = R
        self.requests = deque()
    
    def is_request_allowed(self, timestamp):
        # convert to datetime
        current_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        # compare request time with first request allowed
        while self.requests and current_time - self.requests[0] > timedelta(hours=1):
            self.requests.popleft()
        # if requests list smaller then R then return true
        if len(self.requests) < self.R:
            self.requests.append(current_time)
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
    # read from input
    N, R = map(int, input().split())
    timestamps = [input() for _ in range(N)]
    output = rate_limit_core(N, R, timestamps)
    for value in output:
        print(value)
