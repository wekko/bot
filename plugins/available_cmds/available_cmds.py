from plugin_system import Plugin
from settings import PREFIXES

plugin = Plugin('Помощь',
                usage=['команды - узнать список доступных команд'])


@plugin.on_command('команды', 'помоги', 'помощь')
async def call(msg, args):
    all_usages = ["🔘Доступные команды:🔘\n"]
    usages = ""

    for plugin in msg.vk.get_plugins():
        if not plugin.usage:
            continue

        temp = "🔷" + plugin.name + ":🔷" + "\n"

        for usage in plugin.usage:
            temp += "🔶" + PREFIXES[0] + usage + "\n"

        temp += "\n"

        if len(usages) + len(temp) >= 3072:
            all_usages.append(usages)
            usages = ""

        usages += temp

    all_usages.append(usages)

    if msg.conf and not msg.vk.tokens:
        result = await msg.vk.method("messages.send", {"user_id": msg.user_id, "message": all_usages[0]})

        if result:
            for u in all_usages[1:]:
                await msg.vk.method("messages.send", {"user_id": msg.user_id, "message": u})

            return await msg.answer("Команды отправлены в ЛС!")

    for u in all_usages[:-1]:
        await msg.send(u)

    await msg.answer(all_usages[-1])
