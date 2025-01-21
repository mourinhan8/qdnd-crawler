import fastapi
import uvicorn
from crawler import crawler, get_content
from fastapi.middleware.cors import CORSMiddleware
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_api_token")
async def get_api_token():
    url = "https://mitechcenter.vn/api/account/login"
    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "userNameOrEmailAddress": os.environ.get("ADMIN_USERNAME"),
        "password": os.environ.get("ADMIN_PASSWORD"),
        "rememberMe": True
    }
    response = requests.post(url, headers=headers, json=data)
    cookies = response.cookies
    identity_cookie = cookies.get('.AspNetCore.Identity.Application')

    return {
        "token": identity_cookie
    }


@app.get("/")
async def crawl_and_post():
    urls = crawler()
    data = get_content(urls[0])
    return {
        "image": data["img"],
        "status": 0,
        "priority": 1,
        "postCategoryId": 38,
        "tagIds": [
            8
        ],
        "postTranslations": [
            {
                "title": data["title"],
                "content": data["article_text"],
                "author": "Nhân Sunday",
                "locale": "vi",
                "seoTitle": "",
                "seoSlug": "",
                "seoDescription": "",
                "seoKeywords": ""
            }
        ],
        "publicTime": datetime.datetime.now()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)