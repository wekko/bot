from random import sample

from plugin_system import Plugin

plugin = Plugin("Кто в кого влюблён", usage=['кто кого - поиск парочек в беседе'])


@plugin.on_command('кто кого', 'ктокого')
async def gay_search(msg, args):
    try:
        users = await msg.vk.method('messages.getChatUsers', {'chat_id': msg.cid, 'fields': 'name'})
        love1, love2 = sample(users, 2)
        await msg.answer(f"[id{love1['id']}|{love1['first_name']} {love1['last_name']}] - ❤ Любит ❤ - "
                         f"[id{love2['id']}|{love2['first_name']} {love2['last_name']}]")

    except TypeError:
        await msg.answer("Эту команду можно использовать только в беседе.")
