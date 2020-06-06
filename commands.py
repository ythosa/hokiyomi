import subprocess
import sqlite3
import json
import requests

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
