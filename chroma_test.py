import docx2txt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Read resume
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

# Create Chroma client
client = chromadb.Client()

# Create collection
collection = client.create_collection(
    name="resume"
)

# Add chunks
collection.add(
    documents=chunks,
    embeddings=embeddings.tolist(),
    ids=[str(i) for i in range(len(chunks))]
)

print("Stored", len(chunks), "chunks in ChromaDB")
