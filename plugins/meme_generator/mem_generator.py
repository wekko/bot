import io

import aiohttp
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from plugin_system import Plugin

plugin = Plugin('Генератор мемов', usage=["мем <вверхний текст>\n<нижний текст> - добавляет текст к картинке"])


@plugin.on_init()
async def init(vk):
    plugin.temp_data['fonts'] = []

    with open(f"{plugin.folder}/default.jpg", "rb") as f:
        plugin.temp_data['bg'] = f.read()

    plugin.temp_data['sizes'] = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 90, 80, 70, 60, 50, 40, 30, 20]

    for size in plugin.temp_data['sizes']:
        plugin.temp_data['fonts'].append(ImageFont.truetype(f"{plugin.folder}/Impact.ttf", size))


@plugin.on_command('мем')
async def meme(msg, args):
    if not args:
        return await msg.answer("Пожалуйста, укажите текст для картинки!")

    photo = None

    if msg.brief_attaches:
        for a in await msg.full_attaches:
            if a.type == "photo":
                photo = a

    img = None

    if not photo or not photo.url:
        img = Image.open(io.BytesIO(plugin.temp_data['bg']))

    if not img:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(photo.url) as response:
                img = Image.open(io.BytesIO(await response.read()))

    if not img:
        return await msg.answer('К сожалению, ваше фото исчезло!')

    fonts = plugin.temp_data['fonts']

    strings = msg.text.upper().split("\n")

    if len(strings) < 2:
        strings += [""]

    left_font = 0
    right_font = len(fonts)

    max_h = 0.15
    max_w = 0.9

    fits = False

    while right_font - left_font > 1:
        current_font = (right_font + left_font) // 2

        font = fonts[current_font]

        top_text_size = font.getsize(strings[0])
        bottom_text_size = font.getsize(strings[1])

        if top_text_size[0] >= img.size[0] * max_w or top_text_size[1] >= img.size[1] * max_h \
                or bottom_text_size[0] >= img.size[0] * max_w or bottom_text_size[1] >= img.size[1] * max_h:
            left_font = current_font
        else:
            fits = True

            right_font = current_font

    if fits:
        font = fonts[right_font]
        top_text_size = font.getsize(strings[0])
        bottom_text_size = font.getsize(strings[1])

    else:
        return await msg.answer("Ваш текст не влезает! Простите!")

    top_text_position = img.size[0] / 2 - top_text_size[0] / 2, 0
    bottom_text_position = img.size[0] / 2 - bottom_text_size[0] / 2, img.size[1] - bottom_text_size[1] * 1.17

    draw = ImageDraw.Draw(img)

    outline_range = int(top_text_size[1] * 0.12)
    for x in range(-outline_range, outline_range + 1, 2):
        for y in range(-outline_range, outline_range + 1, 2):
            draw.text((top_text_position[0] + x, top_text_position[1] + y), strings[0], (0, 0, 0), font=font)
            draw.text((bottom_text_position[0] + x, bottom_text_position[1] + y), strings[1], (0, 0, 0), font=font)

    draw.text(top_text_position, strings[0], (255, 255, 255), font=font)
    draw.text(bottom_text_position, strings[1], (255, 255, 255), font=font)

    buffer = io.BytesIO()
    img.save(buffer, format='png')
    buffer.seek(0)

    result = await msg.vk.upload_photo(buffer)

    return await msg.answer('Результат:', attachment=str(result))
