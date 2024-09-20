import os
import chromadb
from database import main as dataFetcher
from query import query_rag as query
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origin = ["*"]


allFiles = os.listdir("./data")
dbClient = chromadb.PersistentClient(path="./database")
# vectorDatabase = Chroma(client=dbClient,collection_name="indian-law", embedding_function=getEmbedding())
try:
    if(os.environ["OPENAI"] and os.environ["GROQ"]):
        pass
    else:
        try:
            envFile = open("./.env")
            allEnvs = envFile.readlines()
            for env in allEnvs:
                env = env.strip()
                os.environ[env.split("=")[0]] =str(env.split("=")[1])
        except:
            raise ValueError("Please set the environment variable from examples")
except:
    pass
collectionCheck = dbClient.list_collections()
if (len(collectionCheck) == 0):
    dataFetcher()
    quit()
else:
    print("Data Exists")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query(BaseModel):
    query: str
@app.post("/")
def root(Query: Query):
        print(Query)
        queryResponse = query(Query.query)
        return {"response": queryResponse.content}
# print(len(vectorDatabase.get()))

# main()