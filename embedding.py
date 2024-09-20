from langchain_openai import OpenAIEmbeddings
import os

def getEmbedding():
    try:
        embedder = OpenAIEmbeddings(api_key=os.environ["OPENAI"], model="text-embedding-3-small")
        return embedder
        
    except:
        raise ValueError("Please set the OPENAI environment variable")

