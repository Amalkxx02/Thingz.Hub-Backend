"""Main Application Entry Point"""
import uvicorn
from app.core import create_app
from app.core.config import settings

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        debug=settings.DEBUG,
    )
