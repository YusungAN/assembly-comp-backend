from db import pinecone, supabase
from util.openai import text_embedding
from typing import Union
import json


def query_pinecone_document(text: str, top_k: int):
    try:
        text_vector = text_embedding(text)
        index = pinecone.Index("assembly-comp")
        query_res = index.query(
            vector=text_vector,
            top_k=top_k,
            include_values=False
        )

        return query_res['matches']
    except:
        return []


def search_document_by_id(id: int):
    fetch = supabase.table('document').select('*').eq('pinecone_id', id).execute()
    res_json = json.loads(fetch.json())['data']
    return res_json[0] if len(res_json) > 0 else None