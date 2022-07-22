from pprint import pprint
from unittest import result

import uvicorn
from fastapi import FastAPI, status
import requests
from pydantic import BaseModel

from schemas import Catalog

app = FastAPI()

# # TODO - add token to environment variable
# REFRESH_TOKEN = "OAUTH2.eyJraWQiOiJkZ0x3cjNRMCIsImFsZyI6IkhTMjU2In0.eyJkYXRhIjoie1" \
#                 "wiaWRcIjpcIjcxMzliODY3LWYxMjMtNDg1MC05NGFiLWE2NDVmNDZiMWM5ZlwifSIs" \
#                 "ImlhdCI6MTY1NzYzMjMxNiwiZXhwIjoxNzIwNzA0MzE2fQ.GSTquygC1Rt9ej4QT_C" \
#                 "Ac4gm98iiQ7zJhl0Yb1afhW4"
#
#
# def access_token(refresh_token: str):
#     # TODO - add data to environment variables
#     url = "https://www.wix.com/oauth/access"
#     body = {
#         "grant_type": "refresh_token",
#         "client_id": "4620bb0a-2113-47db-9d76-1295ad157d1c",
#         "client_secret": "c04609a6-36e1-4813-a4b9-089ea902bd16",
#         "refresh_token": refresh_token,
#     }
#     return requests.post(url, json=body)
#
#
# @app.get("/api/catalogs")
# def catalog_list():
#     url = "https://www.wixapis.com/restaurants/v3/catalogs"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": access_token(REFRESH_TOKEN).json()["access_token"],
#     }
#     response = requests.get(url, headers=headers)
#     return response.json()
#
#
# @app.get("/api/catalogs/{catalog}/manus")
# def manus(catalog: str):
#     catalog = Catalog(**catalog_list()["catalogs"][0])
#     url = f"https://www.wixapis.com/restaurants/v3/catalogs/{catalog.id}/manus"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": access_token(REFRESH_TOKEN).json()["access_token"],
#     }
#     response = requests.get(url, headers=headers)
#     return response.json()


# class WebhookResponse(BaseModel):
#     response: dict


class WebhookDataObject(BaseModel):
    eventType: str
    instanceId: str
    data: str


class WebhookData(BaseModel):
    data: WebhookDataObject


# response_model=WebhookResponse
@app.post("/api/hook", status_code=status.HTTP_200_OK)
def hook(data: WebhookData):
    """
    This is endpoint for receiving webhook requests from the Wix API.
    """
    pprint(data.data.data)
    return {"status": "ok"}


# if __name__ == "__main__":
#     uvicorn.run("main:app",
#                 host="0.0.0.0",
#                 port=8432,
#                 reload=True,
#                 ssl_keyfile="/Users/dmitry/certs/prestowixlocaldev.key",
#                 ssl_certfile="/Users/dmitry/certs/prestowixlocaldev.crt"
#                 )
