from aiogram.filters import Filter
from aiogram.types import Message

from src.utils import is_owner, setup_logger

logger = setup_logger(__name__)


class OwnerFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return is_owner(message.from_user.id)
