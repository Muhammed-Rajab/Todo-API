from pathlib import Path
from app.core.config import settings
from app.routers.todo import todo_router
from app.routers.auth import auth_router
from fastapi import APIRouter, FastAPI, staticfiles

# Arguments to pass to FastAPI class
APP_CONFIGURATION = {
    'debug': True,
    'title': "Todo API",
    'description': "A fastapi-based modern todo api with authentication and many more features",
    'openapi_url': "/legal/openapi.json",
    'docs_url': "/documentation"
}

# App instance
app = FastAPI(**APP_CONFIGURATION)

# Arguments to pass to api_router
API_ROUTER_CONFIGURATION = {
    'prefix': '/api'
}

# Route to include all the api endpoints
api_router = APIRouter(**API_ROUTER_CONFIGURATION)

# Includes other routers to api_router
api_router.include_router(auth_router)
api_router.include_router(todo_router)

# Adds api_router to app
# Note: This should be in the end or routes won't show up
app.include_router(api_router)

# Mounting a static files directory to app
app.mount(
    settings.STATICFILES_URI,
    staticfiles.StaticFiles(
        directory=f"{Path(__file__).resolve().parent}/{settings.STATICFILES_DIR}"), 
        name="static"
    )

if __name__ == "__main__":
    
    import uvicorn
    # Arguments to pass to uvicorn server
    UVICORN_SERVER_CONFIGURATION = {
        'host': "0.0.0.0", 
        'port': 8000, 
        'log_level': "debug"
    }
    # If run directly, then starts uvicorn server
    uvicorn.run(app, **UVICORN_SERVER_CONFIGURATION)