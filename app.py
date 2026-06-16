import streamlit as st
import subprocess

# Google Fonts
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Theme
st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:'Quicksand',sans-serif;
}

.stApp{
    background:#FFF0F5;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#FFD1DC;
}

[data-testid="stSidebar"] *{
    color:#C2185B;
}

/* Title */
h1{
    font-family:'Playfair Display',serif;
}

/* File uploader card */
[data-testid="stFileUploader"]{
    background:rgba(255,255,255,.55);
    border-radius:30px;
    padding:20px;
    box-shadow:0 10px 30px rgba(255,105,180,.15);
}

/* Text input */
.stTextInput input{
    border-radius:25px;
    border:2px solid #FFB6C1;
    box-shadow:0 5px 20px rgba(255,182,193,.25);
}

/* User chat bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
    background:#FF8AB6;
    color:white;
    border-radius:25px;
    padding:20px;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){
    background:#FFF8FC;
    border-radius:25px;
    padding:20px;
    box-shadow:0 5px 20px rgba(255,182,193,.2);
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<h1 style="
color:#C2185B;
text-align:center;
font-size:65px;
font-family:'Playfair Display',serif;
">
🌸 Charisma's Enterprise AI Assistant 🌸
</h1>
""", unsafe_allow_html=True)

# Decorative blossoms
st.markdown("""
<div style="position:fixed;top:120px;left:80px;font-size:60px;opacity:.08;pointer-events:none;">🌸</div>

<div style="position:fixed;top:350px;left:250px;font-size:90px;opacity:.07;pointer-events:none;">🌸</div>

<div style="position:fixed;top:180px;right:180px;font-size:70px;opacity:.08;pointer-events:none;">🌸</div>

<div style="position:fixed;bottom:100px;right:120px;font-size:100px;opacity:.07;pointer-events:none;">🌸</div>

<div style="position:fixed;bottom:200px;left:600px;font-size:60px;opacity:.07;pointer-events:none;">🌸</div>

<div style="position:fixed;top:600px;right:500px;font-size:50px;opacity:.08;pointer-events:none;">🌸</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.header("Uploaded Documents")
uploaded_files = st.file_uploader(
    "Upload PDF or DOCX files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        st.sidebar.write(
            uploaded_file.name
        )
    for uploaded_file in uploaded_files:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        with open(
            f"uploads/{uploaded_file.name}",
            "wb"
        ) as f:
            f.write(uploaded_file.getbuffer())
            
        subprocess.run(
            [
                "python3",
                "ingest_documents.py",
                f"uploads/{uploaded_file.name}"
            ]
        )
question = st.text_input(
    "Ask a question about the document:"
)
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.write("Thinking...")

    st.write("Searching all uploaded documents")

    result = subprocess.run(
    [
        "python3",
        "rag_assistant.py",
        question
    ],
    capture_output=True,
    text=True
)
    
    answer = result.stdout

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):

        st.write(answer)
