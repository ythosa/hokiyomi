import subprocess
import sqlite3
import json
import requests

import db
from exceptions import InvalidAttachments


def add_person_picture(group_id, attachments):
    pic = None
    for pic in attachments:
        if pic["type"] == "photo":
            pic = _get_picture_from_attachments(pic)
            if pic:
                pic = sqlite3.Binary(pic)
                db.insert("images", {
                    "group_id": group_id,
                    "image": pic
                })
            else:
                raise InvalidAttachments("It was some evil there :с Try again :с")

    if not pic:
        raise InvalidAttachments("You didn't attach a photo :c")


def _get_picture_from_attachments(picture):
    picture = picture["photo"]

    max_width = 0
    url = None
    for size in picture["sizes"]:
        if size["width"] > max_width:
            max_width = size["width"]
            url = size["url"]

    pic_path = 'pic.jpg'
    curl_command = f'curl {url} > {pic_path}'

    data = subprocess.run(curl_command, shell=True)

    if data.returncode != 0:
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
    upload_server_url = vk.photos.getMessagesUploadServer(peer_id=chat_id)
    # upload_server_url = json.loads(upload_server_url)
    upload_server_url = upload_server_url["upload_url"]

    cursor = db.get_cursor()
    cursor.execute(
        "select image "
        "from images limit 1"
    )
    photo_bin = cursor.fetchone()[0]

    photo_bin = _write_img(photo_bin)

    photo = {
        'photo': photo_bin
    }
    headers = {
        'content-type': "multipart/form-data",
    }
    res = requests.post(upload_server_url, files=photo, headers=headers)
    res = json.loads(res.text)

    print(res)

    photo = vk.photos.saveMessagesPhoto(
        server=res["server"],
        photo=res["photo"],
        hash=res["hash"],
        photos_list=[]
    )
    photo = json.loads(photo)
    photo_url = "photo" + photo["owner_id"] + "_" + photo["id"]
    return photo_url
