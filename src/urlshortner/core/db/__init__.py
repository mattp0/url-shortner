from .base import Base, metadata_obj

# Convenience re-export so Alembic can target: urlshortner.core.db:Base
__all__ = ["Base", "metadata_obj"]
