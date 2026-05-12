"""
Root entry point for the Job Application API.
Run with: python main.py or uvicorn main:app --reload
"""

import uvicorn
from app.core.settings import get_settings
from app.main import app

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
