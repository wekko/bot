import io

import qrcode
from qrcode.exceptions import DataOverflowError

from plugin_system import Plugin
plugin = Plugin("QRCode генератор",
                usage=["qr [текст / ссылка] - генерирует QR код с вашим текстом"])


@plugin.on_command('qr')
async def command(msg, args):
    if not args:
        await msg.answer('Введите слова или ссылку чтобы сгенерировать qr код')

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(msg.text)

    try:
        qr.make(fit=True)
    except DataOverflowError:
        return await msg.answer('Слишком длинное сообщение!')

    img = qr.make_image()

    buffer = io.BytesIO()
    img.save(buffer, format='png')
    buffer.seek(0)

    result = await msg.vk.upload_photo(buffer)

    return await msg.answer(f'Ваш QR код, с данными: \n "{msg.text}"', attachment=str(result))
