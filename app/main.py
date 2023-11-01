import uvicorn
from api import router as api_router
from fastapi import FastAPI


def create_app():
    """Factory function for creating an app instance"""
    app = FastAPI()
    register_routers(app)
    return app


def register_routers(app: FastAPI):
    """Router includes go here"""
    app.include_router(api_router, prefix="/2fa")


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
