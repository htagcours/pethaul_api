from mistralai import Mistral
from mistralai.models import UserMessage

from .config import env_vars
from .utils import Utils

client = Mistral(api_key=env_vars.MISTRAL_API_KEY)
model = "mistral-small-latest"

def generate_animal_prompt(animal):
    return """Suggest three names for an animal that is a superhero.
                Animal: Cat
                Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
                Animal: Dog
                Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
                Animal: {}
                Names:
                Respond only with the names, no explanation, no formatting.""".format(animal.capitalize()
    )

async def generate_animal_prompt_answer(animal):
    result = ""
    try:
        animal = animal.lower()
        chat_response = await client.chat.complete_async(
            model=model,
            messages=[UserMessage(content=generate_animal_prompt(animal))],
        )
        result = chat_response.choices[0].message.content
        Utils.log_info(f"Result: {result}")
    except Exception as e:
        Utils.log_error(f"Error: {e}")
    return  {"result": result}


async  def generate_answer(message):
    try:
        chat_response = await client.chat.complete_async(
            model=model,
            messages=[UserMessage(content=message)],
        )
        result = chat_response.choices[0].message.content
        Utils.log_info(f"Result: {result}")
        return result
    except Exception as e:
        Utils.log_error(f"Error: {e}")
        return