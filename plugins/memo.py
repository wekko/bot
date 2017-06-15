from database import *
from plugin_system import Plugin


plugin = Plugin('Блокнот',
                usage=['запомни [строка] - запомнить строку',
                       'напомни - напомнить строку'],
                need_db=True)


class Memo(BaseModel):
    uid = peewee.BigIntegerField(unique=True)
    text = peewee.TextField(null=True)

Memo.create_table(True)


@plugin.on_command('запомни', 'запиши')
async def memo_write(msg, args):
    mem, created = await db.get_or_create(Memo, uid=msg.user_id)
    mem.text = msg.text
    await db.update(mem)

    await msg.answer('Вроде запомнил...')


@plugin.on_command('напомни', 'вспомни')
async def memo_read(msg, args):
    mem, created = await db.get_or_create(Memo, uid=msg.user_id)

    if not mem.text:
        await msg.answer('Я ничего не вспомнил!')
    else:
        await msg.answer('Вот что я вспомнил:\n' + mem.text)
