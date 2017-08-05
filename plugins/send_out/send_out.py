from database import *
from plugin_system import Plugin
from utils import schedule_coroutine

plugin = Plugin('Рассылка',
                usage=['разослать [сообщение] - разослать сообщение последним 100 пользователям бота',
                       'разсылать [сообщение] - разсылать сообщение каждые 10 часов последним 100 пользователям бота',
                       'разсылать - не разсылать ничего'])


class SendOutMessage(BaseModel):
    text = peewee.TextField(null=True)

SendOutMessage.create_table(True)


@plugin.on_init()
async def init(vk):
    schedule_coroutine(send_out_periodically())


@plugin.schedule(10 * 60 * 60)
async def send_out_periodically(vk):
    message = await get_or_none(SendOutMessage, id=0)

    if message and message.text:
        await send_out_message(message.text)


async def send_out_message(vk, message):
    values = {"message": message}

    usrs = await db.execute(User.select().limit(100))

    for u in usrs:
        values["user_id"] = u.user_id

        await vk.method("messages.send", values)


@plugin.on_command('разослать')
async def send_out(msg, args):
    if not await get_or_none(Role, user_id=msg.user_id, role="admin"):
        return

    await send_out_message(msg.vk, msg.text)

    return await msg.answer("Готово!")


@plugin.on_command('разсылать')
async def send_out(msg, args):
    if not await get_or_none(Role, user_id=msg.user_id, role="admin"):
        return

    message, created = await db.get_or_create(SendOutMessage, id=0)
    message.text = msg.text
    await db.update(message)

    return await msg.answer("Готово!")
