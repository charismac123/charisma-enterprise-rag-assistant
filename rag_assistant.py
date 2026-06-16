import docx2txt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
import chromadb
import ollama
import sys

# Load document
file_path = None

if len(sys.argv) > 2:
    file_path = sys.argv[2]

if file_path:

    if file_path.endswith(".docx"):

        text = docx2txt.process(
            file_path
        )

    else:

        loader = PyPDFLoader(file_path)

        docs = loader.load()

        text = "\n".join(
            [doc.page_content for doc in docs]
        )


# Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create Chroma collection
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


# Ask a question
import sys

question = sys.argv[1]

# Embed question
question_embedding = model.encode(question)

# Retrieve relevant chunks
if file_path:

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=6,
        where={
            "source": file_path
        }
    )

else:

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=6
    )

    sources = set(
    [
        metadata["source"]
        for metadata in results["metadatas"][0]
    ]
)
#print("\nRetrieved chunks:\n")
#print(results["documents"])
context = "\n".join(results["documents"][0])

source_text = "\n".join(
    [
        f"- {source}"
        for source in sources
    ]
)

# Build prompt
prompt = f"""
Use the information below to answer the question.

Context:
{context}

Question:
{question}

At the end of your answer, include:

Sources:
{source_text}
"""

# Send prompt to Llama3
response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])
