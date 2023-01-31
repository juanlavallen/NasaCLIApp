import os
from io import BytesIO
from pathlib import Path
from PIL import Image
import typer
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
IMAGE_DIR = Path().joinpath('images')

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'), formats=['%Y-%m-%d']
)


@app.command()
def fetch_image(date: datetime = default_date, save: bool = False):
    print('Sending API request...')

    dt = str(date.date())
    url_for_date = f'{API_URL}{API_KEY}&date={dt}'
    response = requests.get(url_for_date)

    response.raise_for_status()

    data = response.json()

    if data['media_type'] != 'image':
        print(f"No image available for {data['date']}")
        return

    url = data['url']
    title = data['title']
    print('Fetching Image...')

    image_response = requests.get(url)
    image = Image.open(BytesIO(image_response.content))

    image.show()

    if save:
        if not IMAGE_DIR.exists():
            os.mkdir(IMAGE_DIR)
        image_name = f'{title}.{image.format}'
        image.save(IMAGE_DIR / image_name, image.format)

    image.close()


if __name__ == '__main__':
    app()
