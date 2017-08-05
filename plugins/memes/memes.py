import random

from plugin_system import Plugin

usage = ['двач - случайная фотка с двача',
         'мемы - случайная фотка из агрегатора мемасов мдк']

plugin = Plugin("Случайные посты из пабликов",
                usage=usage)

stop_list = ['https', 'http', '[club', '[public', '[id']


def any_in(word_list, string):
    return any(i in string for i in word_list)


async def give_memes(msg, group_id):
    """Получает фотографию из случайного поста выбранной группы"""

    text = ''
    photo = None
    tries = 0

    values = {
        'owner_id': group_id,
        'offset': random.randint(1, 1985),
        'count': 10
    }

    while not photo:
        values['offset'] = random.randint(1, 1985)

        data = await msg.vk.method('wall.get', values)
        items = data['items']
        random.shuffle(items)

        for item in items:
            if item["marked_as_ads"] or ("copy_history" in item and item["copy_history"]):
                continue

            if 'attachments' not in item:
                continue

            text = item['text']
            attaches = item['attachments']

            if any_in(stop_list, text) or not attaches:
                continue

            if len(attaches) == 1:
                attach = attaches[0]

                if 'photo' not in attach:
                    continue

                photo = attach['photo']

        tries += 1
        if tries > 100:
            return await msg.answer("Ничего не найдено!")

    owner_id = photo['owner_id']
    photo_id = photo['id']
    access_key = photo['access_key']

    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    await msg.answer(text, attachment=attachment)


@plugin.on_command('двач', '2ch', 'двачик')
async def memes1(msg, args):
    group_id = -22751485
    await give_memes(msg, group_id)


@plugin.on_command('мемы', 'мемасики', 'мемчики', 'мемасик', 'мемосы', 'мемасы')
async def memes2(msg, args):
    group_id = -57846937
    await give_memes(msg, group_id)
