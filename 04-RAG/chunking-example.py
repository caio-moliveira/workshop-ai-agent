#!/usr/bin/env python3
"""
RAG Step 2: Text Chunking
Learn how to split large documents into smaller, manageable pieces
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def replace_t_with_space(list_of_documents):
    """Clean text by replacing tab characters with spaces"""
    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace("\t", " ")
    return list_of_documents


def step2_chunk_text(documents, chunk_size=1000, chunk_overlap=200):
    """
    Step 2: Text Chunking

    This step demonstrates:
    - Why we need to chunk text
    - Chunk size and overlap parameters
    - Text cleaning
    """
    print("✂️  STEP 2: Text Chunking")
    print("=" * 40)

    print("🔧 Chunking parameters:")
    print(f"   Chunk size: {chunk_size} characters")
    print(f"   Chunk overlap: {chunk_overlap} characters")
    print(f"   Overlap ratio: {chunk_overlap / chunk_size:.1%}")

    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )

    print("\n📝 Splitting documents into chunks...")

    # Split documents
    chunks = text_splitter.split_documents(documents)

    # Clean chunks (remove tabs)
    cleaned_chunks = replace_t_with_space(chunks)

    # Display chunking results
    print(f"✅ Created {len(cleaned_chunks)} chunks")

    # Calculate statistics
    chunk_sizes = [len(chunk.page_content) for chunk in cleaned_chunks]
    avg_size = sum(chunk_sizes) / len(chunk_sizes)
    min_size = min(chunk_sizes)
    max_size = max(chunk_sizes)

    print("📊 Chunk statistics:")
    print(f"   Average size: {avg_size:.0f} characters")
    print(f"   Minimum size: {min_size} characters")
    print(f"   Maximum size: {max_size} characters")

    return cleaned_chunks


def show_chunk_samples(chunks, num_samples=10):
    """Show sample chunks for analysis"""
    print("\n🔍 CHUNK SAMPLES")
    print("=" * 40)
    print(f"Showing first {num_samples} chunks for analysis:")

    for i in range(min(num_samples, len(chunks))):
        chunk = chunks[i]
        print(f"\n{'=' * 15} CHUNK {i + 1} {'=' * 15}")
        print(f"📄 Page: {chunk.metadata.get('page', 'Unknown')}")
        print(f"📏 Size: {len(chunk.page_content)} characters")
        print("📝 Content:")
        print("-" * 50)
        print(chunk.page_content)
        print("-" * 50)

        # Quick analysis
        words = len(chunk.page_content.split())
        sentences = (
            chunk.page_content.count(".")
            + chunk.page_content.count("!")
            + chunk.page_content.count("?")
        )

        # Check boundaries
        starts_clean = chunk.page_content[0].isupper() if chunk.page_content else False
        ends_clean = (
            chunk.page_content.strip().endswith((".", "!", "?", '"'))
            if chunk.page_content
            else False
        )

        print(f"📊 {words} words, ~{sentences} sentences")
        if starts_clean and ends_clean:
            print("✅ Clean boundaries")
        else:
            print("⚠️  May have cut boundaries")


def main():
    """Demonstrate text chunking"""
    print("🎓 RAG TUTORIAL - STEP 2: TEXT CHUNKING")
    print("=" * 60)

    # Load document first
    pdf_path = "04-RAG/data/Understanding_Climate_Change.pdf"

    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    print("📄 Loading document...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages")

    # Chunk the text
    chunks = step2_chunk_text(documents, chunk_size=500, chunk_overlap=100)

    # Show chunk samples
    show_chunk_samples(chunks, num_samples=10)

    print("\n📚 KEY LEARNINGS:")
    print("- Documents are split into manageable chunks")
    print("- Overlap prevents information loss at boundaries")
    print("- Clean boundaries improve chunk quality")
    print("- Each chunk maintains source metadata")

    print("\n🎯 Next step: Creating Embeddings (step3_create_embeddings.py)")


if __name__ == "__main__":
    main()
