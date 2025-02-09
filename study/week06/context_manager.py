class ProtectedSection:
    def __init__(self, log=(), suppress=()):
        self.log = log
        self.suppress = suppress
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in self.log:
            self.exception = exc_val
            return self
        elif exc_type in self.suppress:
            return self
        return False

