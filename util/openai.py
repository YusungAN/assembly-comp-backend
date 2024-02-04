from openai import OpenAI, BadRequestError
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))


def summarize_text(text: str):
    try:
        summ_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "아래 글을 한 문단으로 요약해줘. \n\n" + str},
            ]
        )

        summed_text = summ_res.choices[0].message.content
        return summed_text
    except:
        return None


def text_embedding(text: str):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
            encoding_format="float"
        )
        return response.data[0].embedding
    except:
        return None
