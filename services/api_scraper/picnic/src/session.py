from requests import Response, Session


class PicnicAuthError(Exception):
    """Indicates an error when authenticating to the Picnic API."""


class PicnicAPISession(Session):
    AUTH_HEADER = "x-picnic-auth"

    def __init__(self, auth_token: str = None):
        super().__init__()
        # self._auth_token = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyMDMtMDUwLTA3MjAiLCJwYzpjbGlkIjoxLCJwYzpwdjplbmFibGVkIjpmYWxzZSwicGM6bG9naW50cyI6MTYzMTYzNzIwODMwMSwiaXNzIjoicGljbmljLWRldiIsInBjOnB2OnZlcmlmaWVkIjpmYWxzZSwicGM6MmZhIjoiTk9UX1JFUVVJUkVEIiwicGM6cm9sZSI6IlNUQU5EQVJEX1VTRVIiLCJwYzpkaWQiOiI2MTQwYzQ4ODQzMTA4YTRhMzZlNDc0ZjAiLCJleHAiOjE2MzE3MjM2MDgsImlhdCI6MTYzMTYzNzIwOCwianRpIjoiR0RYN0lHVFcifQ.CxRzW_PRJVY8xbcGG6nSHWBL9dmFmb79fq4HZlq48anaUhAelJN6ZWCJLs_XMwJ31cZWGDwUBEwA1b0dPxD7X2mv3w10Om76cVEI9cpwqnNIVZx6WHMSKuzo1m5LYx3XwEhN0mvJI1EWCUcfRyFvk5NTiBImpUJkNkN8tXZGtYrk-rcSxUYahqmZcOxIqhMKLoWgz7JiZCk8B7xG85JNRpjeUi5a0XTmUn49DElB-A_ENPaNB8bVwMvOtt9MvfRq04CMJBWCZ4LsJMMWBialdt_XJ6_-NPGyfWvxqGqE9VElbzx3hzR2z2X6-zfkxy5OEQiOMfn5AgO0QvevFa98YA'
        self._auth_token = auth_token

        self.headers.update(
            {
                "User-Agent": "okhttp/3.9.0",
                "Content-Type": "application/json; charset=UTF-8",
                self.AUTH_HEADER: self._auth_token
            }
        )

    @property
    def authenticated(self):
        """Returns whether the user is authenticated by checking if the authentication token is set."""
        return bool(self._auth_token)

    @property
    def auth_token(self):
        """Returns the auth token."""
        return self._auth_token

    def _update_auth_token(self, auth_token):
        """Update the auth token if not None and changed."""
        if auth_token and auth_token != self._auth_token:
            self._auth_token = auth_token
            self.headers.update({self.AUTH_HEADER: self._auth_token})

    def get(self, url, **kwargs) -> Response:        
        """Do a GET request and update the auth token if set."""
        response = super(PicnicAPISession, self).get(url, **kwargs)
        self._update_auth_token(response.headers.get(self.AUTH_HEADER))

        return response

    def post(self, url, data=None, json=None, **kwargs) -> Response:
        """Do a POST request and update the auth token if set."""
        response = super(PicnicAPISession, self).post(url, data, json, **kwargs)
        
        self._update_auth_token(response.headers.get(self.AUTH_HEADER))

        return response


__all__ = ["PicnicAuthError", "PicnicAPISession"]