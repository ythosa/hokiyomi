# -*- coding: utf-8 -*-
from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id
import re

import commands
import patterns
from exceptions import InvalidAttachments
from tokens import API_TOKEN, CONFIRMATION_CODE

app = Flask(__name__)
vk_session = vk_api.VkApi(token=API_TOKEN)
vk = vk_session.get_api()

confirmation_code = CONFIRMATION_CODE


@app.route('/my_bot', methods=['POST'])
def bot():
    data = request.get_json(force=True, silent=True)

    if not data or 'type' not in data:
        return 'error'

    request_type = data['type']

    if request_type == 'confirmation':
        return confirmation_code
    elif request_type == 'message_new':
        body = data['object']

        message_text = body["text"]
        message_text = message_text.lower()
        chat_id = body['peer_id']

        match = re.match(patterns.ECHO, message_text)
        if match:
            vk.messages.send(
                message='Hi :3',
                random_id=get_random_id(),
                peer_id=chat_id
            )
            return 'ok'

        match = re.match(patterns.ADDPIC, message_text)
        if match:
            attachments = body['attachments']
            user_id = body['from_id']
            try:
                commands.add_person_picture(user_id, attachments)
                vk.messages.send(
                    message='Done 👌🏻',
                    random_id=get_random_id(),
                    peer_id=chat_id
                )
            except InvalidAttachments as e:
                vk.messages.send(
                    message=str(e),
                    random_id=get_random_id(),
                    peer_id=chat_id
                )

    return 'ok'
