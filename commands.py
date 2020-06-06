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
        pass
        # raise InvalidAttachments("You didn't attach a photo :c")


def _get_picture_from_attachments(path):
    url = 'https://api.telegram.org/file/bot' + API_TOKEN + '/' + path

    pic_path = './photos/pic.jpg'
    curl_command = f'curl {url} > {pic_path}'

    data = subprocess.run(curl_command, shell=True)

    if data.returncode != 0:
        print('Error fetching img')
        return None

    with open(pic_path, 'rb') as f:
        data = f.read()

    return data


def _write_img(bin):
    with open('f.jpg', 'wb') as f:
        f.write(bin)

    with open('f.jpg', 'r') as f:
        data = f.read()

    return data


def get_wall_newspaper(vk, chat_id):
    cursor = db.get_cursor()
    cursor.execute(
        "select image "
        "from images limit 1"
    )
