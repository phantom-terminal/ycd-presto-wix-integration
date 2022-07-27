from fastapi import FastAPI, status
import uvicorn

from schemas.wix_input import WebhookResponse, WebhookData

app = FastAPI()


@app.post("/api/hook", response_model=WebhookResponse, status_code=status.HTTP_200_OK)
def hook(data: WebhookData):
    """
    This is endpoint for receiving webhook requests from the Wix API.
    """
    with open("hook.json", "w") as f:
        f.write(str(data))
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8432,
                reload=True,
                ssl_keyfile="/Users/dmitry/certs/prestowixlocaldev.key",
                ssl_certfile="/Users/dmitry/certs/prestowixlocaldev.crt"
                )
