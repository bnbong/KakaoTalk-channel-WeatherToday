from contextvars import ContextVar
from typing import Union, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session

if TYPE_CHECKING:
    from .settings import AppSettings
