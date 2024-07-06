from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
PIXABAY_URL = "https://pixabay.com/api/"

class ImageRequest(BaseModel):
    query: str
    category: str = "animals"
    image_type: str = "photo"
    per_page: int = 5

@lru_cache(maxsize=128)
def fetch_images_from_pixabay():
    params = {
        "key": PIXABAY_API_KEY,
        "q": "spider",
        "category": "animals",
        "image_type": "photo",
        "editors_choice": True,
        "safesearch": True,
    }
    response = requests.get(PIXABAY_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching images from Pixabay")

@app.get("/")
async def get_images():
    try:
        data = fetch_images_from_pixabay()
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
