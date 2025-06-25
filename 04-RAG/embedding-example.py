#!/usr/bin/env python3
"""
RAG Step 3: Creating Embeddings
Learn how to convert text chunks into vector representations
"""

import os
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Configuration
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "mxbai-embed-large:latest"


def replace_t_with_space(list_of_documents):
    """Clean text by replacing tab characters with spaces"""
    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace("\t", " ")
    return list_of_documents


def prepare_chunks():
    """Load and chunk document for embedding demonstration"""
    pdf_path = "04-RAG/data/Understanding_Climate_Change.pdf"

    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return None

    # Load and chunk document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len
    )

    chunks = text_splitter.split_documents(documents)
    cleaned_chunks = replace_t_with_space(chunks)

    return cleaned_chunks


def step3_create_embeddings(chunks):
    """
    Step 3: Creating Embeddings

    This step demonstrates:
    - What embeddings are
    - How to create embeddings from text
    - Vector store creation
    - Embedding properties and dimensions
    """
    print("🧮 STEP 3: Creating Embeddings")
    print("=" * 40)

    print("🔧 Embedding configuration:")
    print(f"   Model: {EMBEDDING_MODEL}")
    print(f"   Ollama URL: {OLLAMA_URL}")
    print(f"   Input chunks: {len(chunks)}")

    # Initialize embedding model
    print("\n🚀 Initializing embedding model...")
    embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model=EMBEDDING_MODEL)

    # Test single embedding first
    print("\n🧪 Testing single embedding...")
    test_text = "Climate change is a global environmental challenge."
    test_embedding = embeddings.embed_query(test_text)

    print("✅ Test embedding created")
    print(f"   Input text: '{test_text}'")
    print(f"   Vector dimension: {len(test_embedding)}")
    print(f"   Vector type: {type(test_embedding)}")
    print(f"   First 5 values: {test_embedding[:5]}")

    # Create vector store from all chunks
    print(f"\n📦 Creating vector store from {len(chunks)} chunks...")
    print("   (This may take a moment...)")

    vector_store = FAISS.from_documents(chunks, embeddings)

    print("✅ Vector store created successfully!")
    print(f"   Total vectors: {len(chunks)}")
    print(f"   Vector dimension: {len(test_embedding)}")

    return vector_store, embeddings


def analyze_embeddings(embeddings):
    """Analyze embedding properties with different text samples"""
    print("\n🔍 EMBEDDING ANALYSIS")
    print("=" * 40)

    # Test different types of text
    test_texts = [
        "Climate change is caused by greenhouse gases.",
        "The effects of global warming are widespread.",
        "Renewable energy sources include solar and wind.",
        "The cat sat on the mat.",  # Unrelated text
        "climate warming temperature greenhouse",  # Keywords only
    ]

    print("📊 Comparing embeddings for different texts:")

    embeddings_list = []
    for text in test_texts:
        embedding = embeddings.embed_query(text)
        embeddings_list.append(embedding)

        # Calculate some basic statistics
        vector_norm = np.linalg.norm(embedding)
        mean_value = np.mean(embedding)

        print(f"\nText: '{text[:50]}...'")
        print(f"   Vector norm: {vector_norm:.4f}")
        print(f"   Mean value: {mean_value:.6f}")

    # Calculate similarity between embeddings
    print("\n🔗 Similarity Analysis:")
    print("   (Using cosine similarity)")

    for i in range(len(test_texts)):
        for j in range(i + 1, len(test_texts)):
            # Calculate cosine similarity
            vec1 = np.array(embeddings_list[i])
            vec2 = np.array(embeddings_list[j])

            similarity = np.dot(vec1, vec2) / (
                np.linalg.norm(vec1) * np.linalg.norm(vec2)
            )

            print(f"   Text {i + 1} ↔ Text {j + 1}: {similarity:.4f}")


def demonstrate_vector_search(vector_store):
    """Demonstrate basic vector similarity search"""
    print("\n🔍 VECTOR SEARCH DEMONSTRATION")
    print("=" * 40)

    # Test queries
    test_queries = [
        "What causes climate change?",
        "Effects of global warming",
        "Renewable energy solutions",
    ]

    for query in test_queries:
        print(f"\n🔎 Query: '{query}'")

        # Perform similarity search
        results = vector_store.similarity_search(query, k=2)

        print(f"   Found {len(results)} similar chunks:")

        for i, doc in enumerate(results):
            print(f"\n   Result {i + 1}:")
            print(f"   Content: {doc.page_content[:150]}...")
            print(f"   Source: Page {doc.metadata.get('page', 'Unknown')}")


def main():
    """Demonstrate embedding creation"""
    print("🎓 RAG TUTORIAL - STEP 3: CREATING EMBEDDINGS")
    print("=" * 60)

    # Prepare chunks
    print("📄 Preparing text chunks...")
    chunks = prepare_chunks()

    if not chunks:
        return

    print(f"✅ Prepared {len(chunks)} chunks")

    try:
        # Create embeddings
        vector_store, embeddings = step3_create_embeddings(chunks)

        # Analyze embeddings
        analyze_embeddings(embeddings)

        # Demonstrate search
        demonstrate_vector_search(vector_store)

        print("\n📚 KEY LEARNINGS:")
        print("- Embeddings convert text into numerical vectors")
        print("- Similar texts produce similar vectors")
        print("- Vector dimension depends on the embedding model")
        print("- FAISS provides fast similarity search")
        print("- Cosine similarity measures vector closeness")
        print("- Vector stores enable semantic search")

        print("\n🎯 Next step: Semantic Search (step4_semantic_search.py)")

    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
        print("💡 Make sure Ollama is running and the model is available:")
        print("   ollama serve")
        print(f"   ollama pull {EMBEDDING_MODEL}")


if __name__ == "__main__":
    main()
