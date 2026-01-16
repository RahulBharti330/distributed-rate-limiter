from threading import Lock


class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.allowed_requests = 0
        self.blocked_requests = 0
        self._lock = Lock()

    def record_allowed(self):
        with self._lock:
            self.total_requests += 1
            self.allowed_requests += 1

    def record_blocked(self):
        with self._lock:
            self.total_requests += 1
            self.blocked_requests += 1

    def snapshot(self):
        with self._lock:
            return {
                "total_requests": self.total_requests,
                "allowed_requests": self.allowed_requests,
                "blocked_requests": self.blocked_requests,
            }


metrics = Metrics()
