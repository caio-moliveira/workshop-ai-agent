#!/usr/bin/env python3
"""
Simple RAG Tutorial - Clean & Minimal
Demonstrates: Processing → Chunking → Embedding → Search → Context → Generation
"""

import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings, Ollama
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import urllib.request

# Load environment variables
load_dotenv()

# Configuration
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "mxbai-embed-large:latest"


def replace_t_with_space(list_of_documents):
    """Clean text by replacing tab characters with spaces"""
    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace("\t", " ")
    return list_of_documents


def download_sample_data():
    """Download sample PDF"""

    os.makedirs("data", exist_ok=True)
    url = "https://raw.githubusercontent.com/NirDiamant/RAG_TECHNIQUES/main/data/Understanding_Climate_Change.pdf"
    filename = "data/Understanding_Climate_Change.pdf"

    if not os.path.exists(filename):
        print("Downloading sample PDF...")
        urllib.request.urlretrieve(url, filename)


class SimpleRAG:
    def __init__(self, use_ollama_llm=False):
        print("🚀 Initializing RAG System...")
        self.embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model=EMBEDDING_MODEL)

        if use_ollama_llm:
            self.llm = Ollama(base_url=OLLAMA_URL, model="deepseek-r1:8b")
            print("   - Using Ollama for everything (no OpenAI needed)")
        else:
            # Use OpenAI for generation only
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            print("   - Using Ollama embeddings + OpenAI generation")

        self.vector_store = None
        self.documents = None
        self.chunks = None

    def step1_process_document(self, file_path):
        """Step 1: Document Processing"""
        print("\n📄 STEP 1: Processing Document")
        loader = PyPDFLoader(file_path)
        self.documents = loader.load()
        print(f"✓ Loaded {len(self.documents)} pages")
        return self.documents

    def step2_chunk_text(self, chunk_size=1000, chunk_overlap=200):
        """Step 2: Text Chunking"""
        print("\n✂️  STEP 2: Chunking Text")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )
        chunks = text_splitter.split_documents(self.documents)
        self.chunks = replace_t_with_space(chunks)
        print(f"✓ Created {len(self.chunks)} chunks")
        return self.chunks

    def step3_create_embeddings(self):
        """Step 3: Create Embeddings"""
        print("\n🧮 STEP 3: Creating Embeddings")
        self.vector_store = FAISS.from_documents(self.chunks, self.embeddings)
        print(f"✓ Vector store created with {len(self.chunks)} embeddings")
        return self.vector_store

    def step4_semantic_search(self, query, k=3):
        """Step 4: Semantic Search"""
        print(f"\n🔍 STEP 4: Semantic Search - '{query}'")
        relevant_docs = self.vector_store.similarity_search(query, k=k)
        print(f"✓ Found {len(relevant_docs)} relevant chunks")
        return relevant_docs

    def step5_enrich_context(self, relevant_docs):
        """Step 5: Context Enrichment"""
        print("\n🎯 STEP 5: Context Enrichment")
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        print(f"✓ Combined context ({len(context)} characters)")
        return context

    def step6_generate_answer(self, query, context):
        """Step 6: Answer Generation"""
        print("\n🤖 STEP 6: Answer Generation")

        prompt_template = """Based on the following context, answer the question concisely and accurately.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Simple chain without structured output
        chain = prompt | self.llm | StrOutputParser()

        answer = chain.invoke({"context": context, "question": query})
        print("✓ Answer generated")
        return answer.strip()

    def full_pipeline(self, query, k=2):
        """Complete RAG Pipeline"""
        print(f"\n🔄 RAG PIPELINE: '{query}'")
        print("=" * 50)

        relevant_docs = self.step4_semantic_search(query, k)
        context = self.step5_enrich_context(relevant_docs)
        answer = self.step6_generate_answer(query, context)

        print("\n📋 RESULT:")
        print(f"Q: {query}")
        print(f"A: {answer}")
        print("=" * 50)

        return {"question": query, "answer": answer}


def main():
    print("🎓 SIMPLE RAG TUTORIAL")
    print("=" * 50)

    # Default to Ollama-only unless user specifically wants OpenAI
    print("Using Ollama for everything (embeddings + generation)")
    print("This requires no API keys!")

    use_openai = input("Use OpenAI for generation? (y/n): ").lower().startswith("y")

    if use_openai and not os.getenv("OPENAI_API_KEY"):
        print("❌ No valid OpenAI API key found. Using Ollama-only mode.")
        use_openai = False

    download_sample_data()
    rag = SimpleRAG(use_ollama_llm=not use_openai)

    # Preprocessing
    rag.step1_process_document("data/Understanding_Climate_Change.pdf")
    rag.step2_chunk_text()
    rag.step3_create_embeddings()

    print("\n🎉 PREPROCESSING COMPLETE!")

    # Queries
    queries = [
        "What is the main cause of climate change?",
        "What are the effects of global warming?",
        "How can we reduce emissions?",
    ]

    for query in queries:
        rag.full_pipeline(query)


if __name__ == "__main__":
    main()
