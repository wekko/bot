import datetime

import hues

from plugin_system import Plugin
from settings import GROUP_ID
from utils import schedule_coroutine, load_settings
from vkplus import Message

plugin = Plugin('Счётчики',
                usage=['обновляет статус бота каждые 5 секунд'])


@plugin.on_init()
async def setup_counter(vk):
    plugin.temp_data['s'] = load_settings(plugin)

    plugin.temp_data['start_time'] = datetime.datetime.now()

    plugin.temp_data['24h'] = datetime.datetime.now()

    plugin.temp_data['messages'] = 0
    plugin.temp_data['messages_24h'] = 0

    plugin.temp_data['commands'] = {}

    if plugin.temp_data['s']['set_status']:
        schedule_coroutine(update_counters(vk))


@plugin.after_command()
async def after(result, msg: Message, args):
    plugin.temp_data['messages'] += 1
    plugin.temp_data['messages_24h'] += 1

    if result is False:
        return

    plugin.temp_data['commands'][msg.command] = plugin.temp_data['commands'].get(msg.command, 0) + 1


@plugin.on_command("статистика", "стата")
async def show(msg, vk):
    uptime = (datetime.datetime.now() - plugin.temp_data['start_time']).total_seconds()

    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)

    top = sorted(plugin.temp_data['commands'].items(), key=lambda x: -x[1])[:5]

    message = f"📈 Статистика бота:\n\n" \
              f"📅 Аптайм: {'%02d:%02d:%02d' % (hours, minutes, seconds)}\n\n" \
              f"📝 Получено сообщений за 24 часа: {plugin.temp_data['messages_24h']}\n" \
              f"📝 Получено сообщений: {plugin.temp_data['messages']}\n\n" \
              f"📈 Самые популярные команды:\n"

    if top:
        message += "📊" + "\n📊".join(f"\"{k}\": {v}" for k, v in top)

    else:
        message += "Нет!"

    await msg.answer(message)


@plugin.schedule(5)
async def update_counters(stopper, vk):
    stopper.sleep = int(plugin.temp_data['s']['time'])

    if datetime.datetime.now() - plugin.temp_data['24h'] >= datetime.timedelta(days=1):
        plugin.temp_data['messages_24h'] = 0
        plugin.temp_data['processed_messages_24h'] = 0
        plugin.temp_data['24h'] = datetime.datetime.now()

    uptime = (datetime.datetime.now() - plugin.temp_data['start_time']).total_seconds()

    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)

    message = f"uptime: {'%02d:%02d:%02d' % (hours, minutes, seconds)} | обработано команд: " \
              f"{plugin.temp_data['messages']} | " \
              f"команд за 24 часа: {plugin.temp_data['messages_24h']}"

    v = {"text": message}
    if GROUP_ID:
        v["group_id"] = GROUP_ID
    elif vk.tokens:
        return hues.error("Невозможно установить статус! Вы не указала ID группы!")

    result = await vk.method("status.set", v)

    if result == 0:
        hues.error("Не удалось установить статус! Для изменения статуса необходи аккаунт администратора группы!")
