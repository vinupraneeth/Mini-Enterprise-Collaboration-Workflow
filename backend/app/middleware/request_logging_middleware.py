import logging

import time

from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("workflow_requests")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = (
            time.perf_counter() -
            start_time
        )

        logger.info(
            "%s %s completed with %s in %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            process_time
        )

        return response
