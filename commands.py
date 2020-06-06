import subprocess
import sqlite3

import db
from exceptions import InvalidAttachments
from tokens import API_TOKEN


def add_person_picture(path, group_id, caption):
    pic = _get_picture_from_attachments(path)

    pic = sqlite3.Binary(pic)
    db.insert("images", {
        "group_id": group_id,
        "caption": caption,
        "image": pic
    })

    if not pic:
        raise InvalidAttachments("You didn't attach a photo :c")


def _get_picture_from_attachments(path):
    url = 'https://api.telegram.org/file/bot' + API_TOKEN + '/' + path

    pic_path = './photos/pic.jpg'
    curl_command = f'curl {url} > {pic_path}'

    data = subprocess.run(curl_command, shell=True)

    if data.returncode != 0:
        raise InvalidAttachments('Something evil has happened :c')

    with open(pic_path, 'rb') as f:
        data = f.read()

    return data


def remove_last(chat_id):
    cur = db.get_cursor()
    cur.execute(
        f"DELETE FROM 'images' WHERE id = "
        f"(SELECT id FROM 'images' WHERE group_id = {chat_id} "
        f"ORDER BY id DESC LIMIT 1)"
    )


def get_wall_newspaper(vk, chat_id):
    db.fetchall('images', 'group_id, image, caption, group_id'.split(', '))
