import time

from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware

from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(
        self,
        app
    ):

        super().__init__(app)

        self.requests = defaultdict(deque)

        self.limits = {
            ("POST", "/auth/login"): (5, 60),
            ("POST", "/auth/register"): (5, 60),
            ("POST", "/auth/refresh"): (10, 60),
            ("POST", "/auth/password-reset/request"): (3, 60),
            ("POST", "/auth/password-reset/confirm"): (5, 60)
        }


    async def dispatch(
        self,
        request,
        call_next
    ):

        limit_config = self.limits.get(
            (
                request.method,
                request.url.path
            )
        )

        if not limit_config:

            return await call_next(request)

        max_requests, window_seconds = limit_config

        client_host = (
            request.client.host
            if request.client
            else "unknown"
        )

        key = (
            client_host,
            request.method,
            request.url.path
        )

        now = time.time()

        request_times = self.requests[key]

        while (
            request_times
            and
            now - request_times[0] > window_seconds
        ):

            request_times.popleft()

        if len(request_times) >= max_requests:

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later."
                }
            )

        request_times.append(now)

        return await call_next(request)
