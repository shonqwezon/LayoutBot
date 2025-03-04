from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import src.messages as msg
from src.keyboards import ownerKb
from src.utils import is_owner, setup_logger

logger = setup_logger(__name__)
user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    if is_owner(message.from_user.id):
        await message.answer(msg.START, reply_markup=ownerKb)
    else:
        await message.answer(msg.START)
