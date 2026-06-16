import docx2txt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Load resume
text = docx2txt.process(
    "documents/Charisma_Chauhan_Microsoft copy.docx"
)

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

# Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# Create Chroma collection
client = chromadb.Client()

collection = client.create_collection(
    name="resume"
)

# Store chunks
collection.add(
    documents=chunks,
    embeddings=embeddings.tolist(),
    ids=[str(i) for i in range(len(chunks))]
)

# QUESTION
query = "Where did Charisma work?"

# Embed question
query_embedding = model.encode(query)

# Search
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=4
)

print(results["documents"])
