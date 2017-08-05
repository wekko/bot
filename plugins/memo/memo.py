import math

from database import *
from plugin_system import Plugin


plugin = Plugin('Блокнот',
                usage=['запомни [строка] - запомнить сообщение',
                       'запомни ещё [строка] - добавить к уже сохранённым сообщениям'
                       'напомни - напомнить сообщение',
                       'забудь - забыть всё'])


class Memo(BaseModel):
    user_id = peewee.BigIntegerField(unique=True)
    text = peewee.TextField(null=True)

Memo.create_table(True)


divider = "<br><br><br><br><br>"


@plugin.on_command('запомни', 'запиши')
async def memo_write(msg, args):
    mem, created = await db.get_or_create(Memo, user_id=msg.user_id)

    attachment = ""
    if msg.brief_attaches:
        attachment = ",".join(str(a) for a in await msg.full_attaches)

    mem.text = msg.text + divider + attachment
    await db.update(mem)

    await msg.answer('Вроде запомнил...')


@plugin.on_command('запомни ещё', 'запиши ещё')
async def memo_add(msg, args):
    mem, created = await db.get_or_create(Memo, user_id=msg.user_id)

    if created:
        return await memo_write(msg, args)

    if len(mem.text) > 9000:
        return await msg.answer(f'Вы сохранили слишком много информации! Больше не получится сохранить!\n'
                                f'Вы можете очистить информацию командой {msg.vk.bot.PREFIXES[0]}забудь')

    parts = mem.text.split(divider)
    old_text = parts[0]
    old_attachment = parts[1]

    attachment = ""
    if msg.brief_attaches:
        attachment = ",".join(str(a) for a in await msg.full_attaches)

    mem.text = old_text + ("\n" + msg.text if msg.text else "") + divider + attachment + "," + old_attachment

    await db.update(mem)

    await msg.answer('Вроде запомнил ещё...')


@plugin.on_command('напомни', 'вспомни')
async def memo_read(msg, args):
    mem, created = await db.get_or_create(Memo, user_id=msg.user_id)

    if not mem.text:
        await db.delete(mem)

        return await msg.answer('Я ничего не вспомнил!')

    parts = mem.text.split(divider)
    text = parts[0]
    attachment = parts[1]

    attachments = attachment.split(",")

    if len(attachments) <= 10:
        return await msg.answer('Вот что я вспомнил:\n' + text, attachment=attachment)

    await msg.send('Вот что я вспомнил:\n' + text, nowait=True)

    amount = math.ceil(len(attachments) / 10)
    for i in range(amount - 1):
        await msg.send('', attachment=",".join(str(a) for a in attachments[i * 10: i * 10 + 10]))

    await msg.answer('', attachment=",".join(str(a) for a in attachments[i * 10: i * 10 + 10]))


@plugin.on_command('забудь')
async def memo_forget(msg, args):
    mem, created = await db.get_or_create(Memo, user_id=msg.user_id)

    await db.delete(mem)

    if not created:
        return await msg.answer('Я всё забыл!')

    await msg.answer('Я ничего и так не помню.')
