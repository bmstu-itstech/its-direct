import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter, ForwardedMessageFilter, IsReplyFilter, ChatTypeFilter
from aiogram.types import Message, ChatType, ParseMode

from core import domain, texts

from common.repository import dp, bot
from services.db.storage import Storage, MessageNotFound
from config import config


DATA_SOURCE_ID_KEY = "source_id"

logger = logging.getLogger(__name__)


@dp.message_handler(IDFilter(chat_id=config.comment_chat_id), ForwardedMessageFilter(is_forwarded=True))
async def handle_ticket_published(message: Message, state: FSMContext, store: Storage):
    ticket_id = extract_ticket_id(message.text)
    await store.update_ticket(ticket_id, group_message_id=message.message_id)


@dp.message_handler(IDFilter(chat_id=config.comment_chat_id), IsReplyFilter(is_reply=True))
async def handle_moderator_answer(message: Message, state: FSMContext, store: Storage):
    _id = message.__dict__["_values"]["message_thread_id"]
    ticket_id = await store.message_ticket_id(_id)
    await send_moderator_answer(message, store, ticket_id, message.text)


async def send_moderator_answer(message: Message, store: Storage, ticket_id: int, answer: str):
    ticket = await store.ticket(ticket_id)
    reply_to_id = None
    try:
        replied_message = await store.message_id(message.reply_to_message.message_id)
        reply_to_id = replied_message.owner_message_id
    except MessageNotFound:
        logger.info(f"Message {reply_to_id} to reply not found")
    sent = await bot.send_message(
        ticket.owner_chat_id,
        texts.ticket.moderator_answer(ticket.id, answer),
        reply_to_message_id=reply_to_id,
        parse_mode=ParseMode.HTML,
    )
    await store.save_message(
        domain.Message(
            chat_id=message.chat.id,
            message_id=message.message_id,
            owner_message_id=sent.message_id,
            reply_to_message_id=sent.reply_to_message.message_id if sent.reply_to_message else None,
            ticket_id=ticket_id,
        )
    )


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), state="*")
async def handle_student_answer(message: Message, state: FSMContext, store: Storage):
    if not message.reply_to_message:
        await message.answer(texts.errors.no_reply)
        return
    ticket_ids = await store.chat_ticket_ids(message.chat.id)
    replied_message = await store.message_by_id(
        ticket_ids=ticket_ids,
        owner_message_id=message.reply_to_message.message_id,
    )
    await send_student_answer(message, store, replied_message, message.text)


async def send_student_answer(message: Message, store: Storage, replied_message: domain.Message, answer: str):
    sent = await bot.send_message(
        config.comment_chat_id,
        texts.ticket.student_answer(answer),
        reply_to_message_id=replied_message.message_id,
        parse_mode=ParseMode.HTML,
    )
    await store.save_message(
        domain.Message(
            chat_id=sent.chat.id,
            message_id=sent.message_id,
            owner_message_id=message.message_id,
            reply_to_message_id=sent.reply_to_message.message_id,
            ticket_id=replied_message.ticket_id,
        )
    )


def extract_ticket_id(s: str) -> int:
    i = s.find(" ")
    j = s.find("\n", i)
    if j < 0:
        j = len(s)
    return int(s[i+1:j])
