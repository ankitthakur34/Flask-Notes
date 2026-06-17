class RateLimitException(Exception):
    def __init__(self, message="Too many requests. Please try again later.", status_code=429):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)