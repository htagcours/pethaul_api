import uuid
import boto3, json
from ..config import env_vars
from ..utils import Utils

def get_table():
    return Utils.get_session().resource("dynamodb").Table(env_vars.DYNAMO_TABLE)


def save_chat_to_dynamodb(message: str, answer: str):
    get_table().put_item(Item={"id": str(uuid.uuid4()),"message": message, "answer": answer})

def get_chats_from_dynamodb() -> list[any]:
    response = get_table().scan()
    return [{"id": item.id, "message": item.message, "answer":item.anwser} for item in response["Items"]]