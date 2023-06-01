import os
import pprint
from pathlib import Path
from dotenv import load_dotenv

import requests
import cloudinary
from bs4 import BeautifulSoup
from cloudinary.uploader import upload

load_dotenv(dotenv_path=Path().absolute().parent / ".env")


def strip_text(text):
    return text if isinstance(text, bool) else text.strip()


def get_data(card):
    name = card.select_one("a.link-ignore").text
    img = card.select_one("img.img-fluid").get("src")
    category = card.select_one("h6 a").get("href")

    staffpick = False
    staffpick_span = card.select("h6")[1].select_one("span")
    if staffpick_span:
        staffpick = staffpick_span.text

    description = card.select_one("p.card-text").text
    link = card.select_one("a.link-ignore").get("href")
    pricing = card.select_one("p.text-end").text.strip(" (?)")
    return {
        "name": strip_text(name),
        "img": strip_text(img),
        "category": strip_text(category),
        "staffpick": staffpick,
        "description": strip_text(description),
        "link": strip_text(link),
        "pricing": strip_text(pricing),
        "show": False,
    }


def upload_images_to_cloudinary(cards):
    authenticate_cloudinary()
    for card in cards:
        data = get_data(card)
        r = upload(data.get("img"), public_id=data.get("name"), folder="whatdevsneed")
        print(r)


def authenticate_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv("cloud_name"),
        api_key=os.getenv("api_key"),
        api_secret=os.getenv("api_secret"),
        secure=True,
    )  # authenticate cloudinary


res = requests.get("https://whatdevsneed.com/")
soup = BeautifulSoup(res.text, "html.parser")
cards = soup.select(".col .card")
upload_images_to_cloudinary(cards)

# for card in cards:
#     data = get_data(card)
#     pprint.pp(data)
