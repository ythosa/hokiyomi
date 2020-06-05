import subprocess
import sqlite3

import db
from exceptions import InvalidAttachments


def add_person_picture(user_id, attachments):
    picture_exist = False
    for a in attachments:
        if a["type"] == "photo":
            picture_exist = True
            break

    if picture_exist:
        pic = _get_picture_from_attachments(attachments)
        pic_binary = sqlite3.Binary(pic)
        db.insert("images", {
            "user_id": user_id,
            "image": pic_binary
        })
    else:
        raise InvalidAttachments("You didn't attach a photo :c")


def _get_picture_from_attachments(attachments):
    picture = attachments
    width, height = picture.width, picture.height

    url = ""
    for size in picture["sizes"]:
        if size["width"] == width and size["height"] == height:
            url = size["url"]

    curl_command = f'curl {url} > data.json'

    data = subprocess.run(curl_command, shell=True)

    if data.returncode != 0:
        exit('It was some evil there :( Try again :(')

    with open('data.json', 'rb', encoding='cp1251') as f:
        data = f.read()

    return data
