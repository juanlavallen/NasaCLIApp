import os
import typer
import requests
import asyncio
import httpx
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

async def get_images(urls):
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_tasks(get_image(client, url)))
        
        images = asyncio.gather(*tasks)
        return images

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

    urls = [d['url'] for d in data if d['media_type'] == 'image']
    titles = [d['title'] for d in data if d['media_type'] == 'image']

    for res in data:
        if res['media_type' != 'image']:
            print(f"No image available for {res['date']}")

    images = asyncio.run(get_images(urls))

    for i, image in enumerate(images):
        image.show()

        if save:
            save_image_to_filesystem(image, titles[i])

        image.close()


if __name__ == '__main__':
    app()
