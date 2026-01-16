class FakeRequest:
    def __init__(self, headers, path):
        self.headers = headers
        self.url = type("URL", (), {"path": path})
