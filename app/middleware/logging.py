"""
Logging middleware for request/response tracking.
"""

import logging
import time
from typing import Callable

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """
    Log incoming requests and outgoing responses.
    
    Args:
        request: The incoming HTTP request
        call_next: The next middleware or route handler
        
    Returns:
        The HTTP response
    """
    # Record start time
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"{request.method} {request.url.path}")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response with timing
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response
