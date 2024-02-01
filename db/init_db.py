from pinecone import Pinecone
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

pinecone = Pinecone(api_key=os.getenv('PINECONE_KEY'))
supabase: Client = create_client(os.getenv('SUPA_URL'), os.getenv('SUPA_KEY'))