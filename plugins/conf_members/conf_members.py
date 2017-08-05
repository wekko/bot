import random

from database import *
from plugin_system import Plugin
from utils import load_settings

plugin = Plugin('Узнать кто находится в беседе',
                usage=['кто здесь - узнать членов беседы в которой вы введёте эту команду.'])

@plugin.on_init()
async def init(vk):
    plugin.temp_data = load_settings(plugin)

@plugin.on_command('кто здесь', 'ктоздесь')
async def whoishere(msg, args):
    users = ""
    emojis = ['😏', '😄', '😠', '😆', '🤐', '😝', '🤔', '😎', '😐', '🙁',
              '😨', '🤔', '😠', '😝', '😘', '😗', '😙', '😙', '😟']
    try:
        all_users = await msg.vk.method("messages.getChatUsers", {'chat_id': msg.cid, 'fields': 'name,online'})

        random.seed(msg.cid)

        for user in all_users:
            if await get_or_none(Role, user_id=user['id'], role="admin"):
                emoji = f"👑 "
            else:
                emoji = random.choice(emojis) + " "

            if plugin.temp_data['show']:
                users += f"{emoji} [id{user['id']}|{user['first_name']} {user['last_name']}] " \
                         f"{' - онлайн' if user['online'] else ''}\n"

            elif user['online']:
                users += f"{emoji} [id{user['id']}|{user['first_name']} {user['last_name']}]\n"

        if plugin.temp_data['show']:
            await msg.answer(f'👽 Состав беседы:\n' + users)

        else:
            await msg.answer(f'👽 Сейчас в беседе:\n' + users)

    except TypeError:
        await msg.answer("Эту команду можно использовать только в беседе.")

