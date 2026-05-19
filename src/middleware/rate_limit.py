import time
from collections import defaultdict
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.config import settings


class InMemoryRateLimiter:
    """Fixed-window rate limiter keyed by client IP."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        hits = [t for t in self._hits[key] if t > window_start]
        if len(hits) >= self.max_requests:
            self._hits[key] = hits
            return False
        hits.append(now)
        self._hits[key] = hits
        return True

    def retry_after_seconds(self, key: str) -> int:
        hits = self._hits.get(key, [])
        if not hits:
            return self.window_seconds
        oldest = min(hits)
        wait = int(self.window_seconds - (time.time() - oldest)) + 1
        return max(1, wait)


_limiter = InMemoryRateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Apply rate limits to chat endpoints."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        if request.url.path.startswith("/chat") and request.method == "POST":
            client_ip = request.client.host if request.client else "unknown"
            if not _limiter.is_allowed(client_ip):
                retry_after = _limiter.retry_after_seconds(client_ip)
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": (
                            f"Rate limit exceeded: "
                            f"{settings.rate_limit_requests} requests per "
                            f"{settings.rate_limit_window_seconds}s."
                        )
                    },
                    headers={"Retry-After": str(retry_after)},
                )
        return await call_next(request)
