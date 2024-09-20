import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAI
import os
from embedding import getEmbedding
from langchain_groq import ChatGroq

CHROMA_PATH = "./database"

PROMPT_TEMPLATE = """
You are a Indian law expert, We have documents and data as vector embeddings which has information about the new Bhartiya Nyaya Sanhita and THE BHARATIYA SAKSHYA BILL. The document is in English. You have to answer the questions below with the new documents and your knowledge and also compare the difference between old and new law system. Do not mention that document was provided and be confident about indian law system and the document data, Do not mention the source of the document.

Here is The Relevant Data about the query and topic ${context}
---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = getEmbedding()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function, collection_name="indian-law")
    db.get()
    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=6)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OpenAI(api_key=os.environ["OPENAI"])
    
    llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ["GROQ"]
    # other params...
)
    response_text = llm.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return response_text


# if __name__ == "__main__":
#     main()
