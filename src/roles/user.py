from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject

import src.messages as msg
from src.db import (
    get_handled_docs_len,
    get_response,
    get_total_docs_len,
    update_response,
)
from src.keyboards import get_gb_kb, ownerKb
from src.utils import is_owner, setup_logger

logger = setup_logger(__name__)
user = Router()


class BodyField:
    ANSWER = "Ответ AI (уточнение)"
    QUESTION = "Уточненный вопрос пользователя"


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    if is_owner(message.from_user.id):
        await message.answer(msg.START, reply_markup=ownerKb)
    else:
        await message.answer(msg.START)


@user.message(Command("myid"))
async def show_id(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(msg.YOUR_ID.format(message.from_user.id))


@user.message(Command("tasks"))
@user.callback_query(F.data.startswith("answer_"))
async def get_task(event: TelegramObject, state: FSMContext):
    if isinstance(event, CallbackQuery):
        await event.bot.delete_message(event.from_user.id, event.message.message_id)
        ans = event.data.split("_")[1]
        id = event.data.split("_")[2]
        await update_response(id, event.from_user.id, ans)

    doc = await get_response(event.from_user.id)
    if isinstance(event, CallbackQuery):
        message = event.message
    elif isinstance(event, Message):
        message = event
    if not doc:
        await message.answer(msg.GAME_OVER)
        return
    await message.answer(
        msg.ARENA.format(
            question=doc["body"][BodyField.QUESTION],
            answer=doc["body"][BodyField.ANSWER],
        ),
        reply_markup=get_gb_kb(doc["_id"]),
    )


@user.message(Command("status"))
async def get_status(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        msg.STATUS.format(
            now=await get_handled_docs_len(), total=await get_total_docs_len()
        )
    )
