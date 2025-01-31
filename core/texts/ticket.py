from datetime import datetime

from core.domain import TicketRecord
from common.repository import compiler


greet = "\n".join((
    "👋 Привет, Бауманец!",
    "Рады видеть тебя в нашем боте! Здесь ты можешь:",
    "🔹 Задать любые вопросы, которые тебя волнуют.",
    "🔹 Сообщить о возникшей проблеме.",
    "🔹 Предложить свою идею.",
))

create_ticket = \
    "Чтобы создать обращение, просто нажми кнопку ниже."

choice_issue = "\n".join((
    "Выбери тип обращения:",
    "🔧 Проблема – расскажи, что требует решения.",
    "❓ Вопрос – задай интересующий тебя вопрос.",
    "💡 Предложение – поделись своими идеями и инициативами!",
))

choice_category = \
    "Выбери направление, с которым связано твоё обращение."

choice_privacy = "\n".join((
    "🤫 Хотите отправить обращение анонимно?",
    "Конфиденциальность – наш лучший друг после вас!"
))

input_full_name = "\n".join((
    "✍️ Напиши своё полное ФИО",
    "Пожалуйста, укажи имя и фамилию, и если есть — добавь отчество.",
    "Пример: Иванов Иван Иванович"
))


input_study_group = \
    "🎓 Напиши номер своей учебной группы. Формат ввода: ИУ13-13Б."

input_text = \
    "📩 Опиши ниже свой вопрос или проблему:"

choice_approve = \
    "👀 Проверь, всё ли введено правильно. Подтверждаешь данные?"


ticket_channel_template = compiler.compile("\n".join((
    "<b>Обращение</b> <code>{{as_ticket_id ticket.id }}</code>",
    "",
    "📌 Тип: {{as_tag ticket.issue}}",
    "📂 Категория: {{as_tag ticket.category}}",
    "{{#if ticket.owner}}",
    "👤 Отправитель: {{ticket.owner.full_name}}",
    "🎓 Учебная группа: {{ticket.owner.study_group}}",
    "{{else}}",
    "👤 Отправитель: Анонимно",
    "{{/if}}",
    "🕒 Дата отправки: {{as_date ticket.opened_at}}",
    "--------------------------------------------",
    "📩 Текст обращения:",
    "{{ticket.text}}",
)))

answer_moderator_template = compiler.compile("\n".join((
    "💬 Ответ администратора на обращение <code>{{as_ticket_id ticket_id}}</code>:",
    "{{answer}}"
)))

answer_student_template = compiler.compile("\n".join((
    "💬 Ответ:",
    "{{answer}}"
)))

ticket_sent_template = compiler.compile("\n".join((
    "Твоё обращение отправлено! Ему присвоили номер <code>{{as_ticket_id ticket_id}}</code>",
)))


def ticket_sent(ticket_id: int) -> str:
    return ticket_sent_template(
        {
            "ticket_id": ticket_id,
        },
        helpers={
            "as_ticket_id": as_ticket_id,
        }
    )


def ticket_channel(ticket: TicketRecord) -> str:
    return ticket_channel_template(
        {
            "ticket": ticket,
        },
        helpers={
            "as_tag":       as_tag,
            "as_date":      as_date,
            "as_ticket_id": as_ticket_id,
        }
    )


def student_answer(answer: str) -> str:
    return answer_student_template({
        "answer": answer,
    })


def moderator_answer(ticket_id: int, answer: str) -> str:
    return answer_moderator_template(
        {
            "ticket_id": ticket_id,
            "answer": answer,
        },
        helpers={
            "as_ticket_id": as_ticket_id,
        }
    )


def as_tag(this, s: str) -> str:
    return "#" + s.lower().replace(" ", "")


def as_date(this, dt: datetime, date_format: str = None) -> str:
    return datetime.strftime(dt, date_format or "%d.%m.%Y %H:%M:%S")

def as_ticket_id(this, _id: int):
    return f"{_id:04d}"
