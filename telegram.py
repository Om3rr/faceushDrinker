import requests
import random
import string
from PIL import Image
import io
from constants import *


def notify(message, reply=None):
    res = requests.post(f"https://api.telegram.org/bot{API_KEY}/sendMessage", {"chat_id": CHAT_ID, "text": message, "reply_to_message_id": reply})


def sendPhoto(path, caption, message_id=''):
    img = Image.open(path, mode='r')
    bytesArray = io.BytesIO()
    img.save(bytesArray, format="PNG")
    bytesArray = bytesArray.getvalue()
    data = {"chat_id": CHAT_ID, "caption": caption}
    if message_id != '':
        data['message_id'] = message_id
    res = requests.post(f"https://api.telegram.org/bot{API_KEY}/sendPhoto", data, files=dict(photo=bytesArray))
    response = res.json()
    if response['ok']:
        return response['result']['message_id']
    else:
        return False

def random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))