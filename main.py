import os
import typer
import requests
from datetime import datetime
from dotenv import load_dotenv
from helpers import save_image_to_filesystem, url_query_params, get_image

load_dotenv()

app = typer.Typer()

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'), formats=['%Y-%m-%d']
)


@app.command()
def fetch_image(
    date: datetime = default_date,
    save: bool = False,
    start: datetime = typer.Option(None),
    end: datetime = typer.Option(None)
):
    print('Sending API request...')

    query_params = url_query_params(date, start, end)
    response = requests.get(API_URL, params=query_params)

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        data = [data]

    for res in data:
        if res['media_type'] != 'image':
            print(f"No image available for {data['date']}")
            continue

        url = res['url']
        title = res['title']

        print('Fetching Image...')

        image = get_image(url)
        image.show()

        if save:
            save_image_to_filesystem(image, title)

        image.close()


if __name__ == '__main__':
    app()
