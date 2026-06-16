import docx2txt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

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

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert chunks to vectors
embeddings = model.encode(chunks)

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
