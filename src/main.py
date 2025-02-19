import json
from botocore.vendored import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from mangum import Mangum

from src.database.db import save_chat_to_dynamodb
from src.mistral_proxy import generate_animal_prompt_answer, generate_answer
from src.utils import Utils

TELEGRAM_TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)

def send_message(text, chat_id):
    final_text = "You said: " + text
    url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    requests.get(url)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    chat_id = body['message']['chat']['id']
    text = body['message']['text']
    send_message(text, chat_id)
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent!')
    }

@asynccontextmanager
async def app_lifespan(application: FastAPI):
    Utils.log_info("Starting the application")
    yield


app = FastAPI(
    title="Pethaul API",
    description="Pethaul API description",
    version="1.0.0",
    lifespan=app_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/prompt")
async def prompt():
    return {"msg": "Hello", "response": ""}



@app.post("/guest_name")
async def guest_name(animal: str):
    try:
        animal = animal.lower()
        Utils.log_info(animal)
        result = await generate_animal_prompt_answer(animal)
        Utils.log_info(f"Result: {result}")
        return {"result": result}
    except Exception as e:
        Utils.log_error(f"Error: {e}")
        return

@app.post("/chat")
async def chat(message: str):
    try:
        Utils.log_debug(message)
        result = await generate_answer(message)
        save_chat_to_dynamodb(message, result)
        return {"result": result}
    except Exception as e:
        Utils.log_error(f"Error: {e}")
        return

@app.get("/chats")
async def chat(message: str):
    return


handler = Mangum(app)