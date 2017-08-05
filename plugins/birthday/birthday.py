import datetime

from plugin_system import Plugin
from utils import plural_form, age
from vkplus import MAX_MESSAGE_LENGTH

plugin = Plugin('Дни рождения в группе',
                usage=["др [id] - узнать дни рождения в группе с id",
                       "др - узнать дни рождения в беседе"])


MAX_USERS_IN_GROUP = 1000


@plugin.on_command('др')
async def check(msg, args):
    if len(args) > 0:
        members = []

        temp = [1]
        offset = 0

        while True:
            result = await msg.vk.method("groups.getMembers", {"group_id": args[0],
                                                               "offset": offset,
                                                               "fields": "bdate"})

            if not result["items"]:
                if offset == 0:
                    return await msg.answer("Не удалось получить сообщество или оно пусто!")

                break

            members += result["items"]

            offset += 1000

            if result["count"] > MAX_USERS_IN_GROUP:
                await msg.answer(f"Вы пытаетесь узнать дни рождения слишком многих людей!\n"
                                 f"Будут показана лишь {MAX_USERS_IN_GROUP} из пользователей")

            break

        message = f"Дни рождения пользователей в группе \"{args[0]}\" ✨:\n"

    else:
        if not msg.conf:
            members = await msg.vk.method("users.get", {"user_ids": msg.user_id, "fields": "bdate"})

            message = f"Ваш день рождения ✨:\n"

        else:
            members = await msg.vk.method("messages.getChatUsers", {"chat_id": msg.cid, "fields": "bdate"})

            message = f"Дни рождения пользователей в беседе ✨:\n"

    data = []

    now = datetime.datetime.today().date()

    for m in members:
        if "bdate" not in m or "deactivated" in m:
            continue

        try:
            if m['bdate'].count(".") > 1:
                year = True
                user_date = datetime.datetime.strptime(m['bdate'], '%d.%m.%Y').date()

            else:
                year = False
                user_date = datetime.datetime.strptime(m['bdate'], '%d.%m').date()

        except ValueError:
            continue

        try:
            check_date = user_date.replace(year=now.year)
        except ValueError:
            check_date = user_date + (datetime.date(now.year, 1, 1) - datetime.date(user_date.year, 1, 1))

        difference = check_date - now

        if difference.days < 0:
            check_date = check_date.replace(year=now.year + 1)

            difference = check_date - now

        bdate_in = " (будет через " + plural_form(difference.days, ("день", "дня", "дней")) + ")"

        if year:
            bdate_in = bdate_in[:-1] + ", исполнится " + plural_form(age(user_date) + 1, ("год", "года", "лет")) + ")"

        data.append((" 🌍 " + m["first_name"] + " " + m["last_name"] + ": "
                     + user_date.strftime("%m.%d") + bdate_in + "\n",
                     difference.days))

    messages = (d[0] for d in sorted(data, key=lambda x: x[1]))

    for m in messages:
        if len(message) + len(m) >= MAX_MESSAGE_LENGTH:
            await msg.send(message)

            message = ""

        message += m

    return await msg.answer(message)
