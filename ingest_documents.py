import sys
import docx2txt
import chromadb

from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# File path
file_path = sys.argv[1]

# Load document
if file_path.endswith(".docx"):

    text = docx2txt.process(
        file_path
    )

else:

    loader = PyPDFLoader(
        file_path
    )

    docs = loader.load()

    text = "\n".join(
        [doc.page_content for doc in docs]
    )
    # Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(
    text
)# Create embeddings
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    chunks
)
# Create Chroma collection
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)
# Store chunks
collection.upsert(
    documents=chunks,
    embeddings=embeddings.tolist(),
    ids=[
        f"{file_path}_{i}"
        for i in range(len(chunks))
    ],
    metadatas=[
        {
            "source": file_path
        }
        for _ in chunks
    ]
)