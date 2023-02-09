import os
from io import BytesIO
from pathlib import Path
from typing import Dict
from PIL import Image
import requests

IMAGE_DIR = Path().joinpath('images')

def url_query_params(datetime, start, end) -> Dict:
    if start:
        params = {'start_date': str(start.date())}

        if end:
            params['end_date'] = str(end.date())

        return params
    else:
        return {'date': str(datetime.date())}


def get_image(url: str) -> Image:
    image_response = requests.get(url)
    image = Image.open(BytesIO(image_response.content))
    return image


def save_image_to_filesystem(image: Image, title: str):
    if not IMAGE_DIR.exists():
        os.mkdir(IMAGE_DIR)

    image_name = f'{title}.{image.format}'
    image.save(IMAGE_DIR / image_name, image.format)
