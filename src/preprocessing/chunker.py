from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text):
    return RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", " ", ""]
    ).split_text(text)
