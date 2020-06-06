import base64
import subprocess
# import sqlite3

# import db
from exceptions import InvalidAttachments
import test_db


def add_person_picture(group_id, attachments):
    pic = None
    for a in attachments:
        if a["type"] == "photo":
            pic = a
            break

    if pic:
        pic = _get_picture_from_attachments(pic)
        # pic_binary = sqlite3.Binary(pic)
        # db.insert("images", {
        #     "group_id": group_id,
        #     "image": pic_binary
        # })
        # pic = base64.b64encode(pic)

        test_db.add_group_pic(group_id, str(pic))
    else:
        raise InvalidAttachments("You didn't attach a photo :c")


def _get_picture_from_attachments(picture):
    picture = picture["photo"]

    max_width = 0
    url = None
    for size in picture["sizes"]:
        if size["width"] > max_width:
            max_width = size["width"]
            url = size["url"]

    curl_command = f'curl {url} > data.json'

    data = subprocess.run(curl_command, shell=True)

    if data.returncode != 0:
        exit('It was some evil there :( Try again :(')

    with open('data.json', 'rb') as f:
        data = f.read()

    return data
