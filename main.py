from io import BytesIO
import os
from PIL import Image
import typer
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'), formats=['%Y-%m-%d']
)


@app.command()
def fetch_image(date: datetime = default_date):
    print('Sending API request...')

    dt = str(date.date())
    url_for_date = f'{API_URL}{API_KEY}&date={dt}'
    response = requests.get(url_for_date)

    response.raise_for_status()

    url = response.json()['url']
    print('Fetching Image...')

    image_response = requests.get(url)
    image = Image.open(BytesIO(image_response.content))

    image.show()


if __name__ == '__main__':
    app()
