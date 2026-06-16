import docx2txt
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Read the resume
text = docx2txt.process(
    "documents/Charisma_Chauhan_Microsoft copy.docx"
)

# Create the splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Split into chunks
chunks = splitter.split_text(text)

# Print how many chunks we made
print("Number of chunks:", len(chunks))

# Print the first chunk
print("\nFirst chunk:\n")
print(chunks[0])
