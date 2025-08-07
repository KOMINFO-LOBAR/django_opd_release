from .celery import app as celery_app

__all__ = ("celery_app",)

# untuk memastikan celery di load oleh system