from typing import List, Optional
from langchain.docstore.document import Document
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import TokenTextSplitter


class CleanTextLoader(TextLoader):
    """Load text files."""

    def __init__(self, file_path: str, encoding: Optional[str] = None):
        """Initialize with file path."""
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            text = f.read()
        text = self.clean_text(text)
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]

    def clean_text(self, text):
        # remove leading and trailing whitespace from each line
        lines = (line.strip() for line in text.splitlines())
        # replace two or more whitespace characters with a single space
        text = ' '.join(line for line in lines)
        text = ' '.join(text.split())
        # remove two or more consecutive empty lines
        text = '\n'.join(line for line in text.splitlines() if line.strip())
        return text


def load_n_split(path, splitter = "token"):
    """
    path: direcotry path having text files.
    Thus function read text files, clean it and then split it into chunks
    """
    loader = DirectoryLoader(path, glob="**/*.txt",loader_cls= CleanTextLoader)
    documents = loader.load() 
    if splitter == "token":
        text_splitter = TokenTextSplitter(   chunk_size=80, chunk_overlap=20)
    else:
        print('invalid splitter')
    doct_text = text_splitter.split_documents(documents)
    return doct_text
