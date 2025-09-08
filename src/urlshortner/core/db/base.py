from __future__ import annotations

import uuid
from typing import Annotated

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column

# Naming conventions keep Alembic diffs stable
metadata_obj = MetaData(
    naming_convention={
        "ix": "ix__%(table_name)s__%(column_0_label)s",
        "uq": "uq__%(table_name)s__%(column_0_name)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": "fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk__%(table_name)s",
    }
)


class Base(DeclarativeBase):
    metadata = metadata_obj


UuidPK = Annotated[uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]
