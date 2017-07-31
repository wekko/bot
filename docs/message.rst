
##########################
Описание объекта сообщения
##########################

::

    @plugin.on_message()
    async def command(msg: Message, args):
        pass



.. py:class:: Message

    .. py:function:: answer(msg: str, \*\*additional_values)

       (Сопрограмма)
       Функция, посылающая сообщение ``msg`` отправителю сообщения с дополнительными параметрами ``additional_values``.
       Стоит использовать в случае, когда это последнее или единственное сообщение от плагина.

    .. py:function:: send(msg: str, \*\*additional_values)

       (Сопрограмма)
       Функция, посылающая сообщение ``msg`` отправителю сообщения с дополнительными параметрами ``additional_values``.

    .. py:attribute:: vk

       экземпляр VkPlus, объект, через который бот взаимодействует с ВКонтакте.

    .. py:attribute:: conf

       True, если сообщение пришло из беседы, иначе False

    .. py:attribute:: user

       Экземпляр User из базы данных

    .. py:attribute:: cid

       Id беседы или None, если сообщение не из беседы

    .. py:attribute:: user_id

       Id автора сообщения

    .. py:attribute:: peer_id

       Отправитель (id беседы, пользователя без разбора, лучше использовать user_id и cid)

    .. py:attribute:: text

       Сообщение пользователя без префикса и команды

    .. py:attribute:: body

       Сообщение пользователя

    .. py:attribute:: prefix

       True, если сообщение содержит префикс, иначе False

    .. py:attribute:: is_out

       True, если сообщение исходящее, иначе False

    .. py:attribute:: timestamp

       UNIX-время отправки сообщения

    .. py:attribute:: brief_attaches

       Индикатор вложений сообщения, содержит вложения, но не гарантировано, что все и не гарантировано, что они будут содержать access_key

    .. py:attribute:: full_attaches

       (Сопрограмма, атрибут)
       которая возвращает все вложения

    .. py:attribute:: brief_forwarded

       Список с ID пересылаемыми сообщениями формата (id сообщения, id пересылаемых сообщении).

    .. py:attribute:: full_forwarded

       (Сопрограмма, атрибут)
       Список с ID пересылаемыми сообщениями формата (id сообщения, id пересылаемых сообщении).

    .. py:attribute:: msg_id

       Id сообщения

    .. py:attribute:: command

       Команда в сообщении, если присутствует