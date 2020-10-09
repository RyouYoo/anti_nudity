import discord
import uuid
import json
import requests
from requests_toolbelt import MultipartEncoder

class CheckNudity():
    def __init__(self, _id, token):
        self.id = str(_id)
        self.token = token
        self.image_id = None

    def isItNudity(self):
        url = f"https://discord.com/api/v8/channels/{self.id}/messages"
        headers = {
            "authorization": self.token,
        }
        files = {
            "file": (f"{self.image_id}.jpg", open(f"./images/{self.image_id}.jpg", "rb")),
            "Content-Type": "image/jpeg",
            "content": "",
            "tts": "false"
        }
        m = MultipartEncoder(files)
        headers["content-type"] = m.content_type
        r = requests.post(url=url,headers=headers, data=m)
        try:
            if r.json()["message"] == "Explicit content cannot be sent to the desired recipient(s)":
                return True
        except Exception:
            return False

    def downloadImage(self, image_url):
        self.image_id = str(uuid.uuid4()) 
        with open(f"./images/{self.image_id}.jpg", "wb") as image:
            response = requests.get(image_url, stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break
                image.write(block)

with open("./config.json", "r") as config:
    config = json.load(config)

nudity = CheckNudity(config["channel_id"],config["user_token"])

nudity.downloadImage("[IMAGE URL]")

if nudity.isItNudity():
    print("It's nude!")
else:
    print("It's not nude!")