import time
from venv import logger

import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def get_status(user_id):
    url = "https://api.vk.com/method/users.et"
    params = {
        "user_ids": user_id,
        "v": os.getenv("vk_api_version"),
        "access_token": os.getenv("vk_token"),
        "fields": "online",
    }
    try:
        response = requests.post(url, params=params).json().get("response")[0]
        res = response["online"]
    except Exception as e:
        logger.exception(e)
        res = e
    return res


def sms_sender(sms_text):
    token = os.getenv("tw_token")
    account_sid = os.getenv("tw_account_sid")
    from_ = os.getenv("tw_phone")
    to_ = os.getenv("my_phone")
    client = Client(account_sid, token)
    try:
        message = client.messages.create(body=sms_text, from_=from_, to=to_)
        res = message.sid
    except Exception as e:
        logger.log(e)
        res = e
    return res


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f"{vk_id} сейчас онлайн!")
            break
        time.sleep(5)
