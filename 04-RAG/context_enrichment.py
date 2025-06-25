#!/usr/bin/env python3
"""
RAG Step 5: Context Enrichment
Learn how to combine and prepare retrieved information for answer generation
"""

import os
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


def prepare_vector_store():
    """Prepare vector store for context enrichment demonstration"""
    pdf_path = "data/Understanding_Climate_Change.pdf"

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

    # Create embeddings and vector store
    embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model=EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(cleaned_chunks, embeddings)

    return vector_store


def step5_enrich_context(relevant_docs, query):
    """
    Step 5: Context Enrichment

    This step demonstrates:
    - Combining multiple retrieved chunks
    - Creating coherent context
    - Analyzing context quality
    - Preparing for answer generation
    """
    print("🎯 STEP 5: Context Enrichment")
    print("=" * 40)

    print(f"🔍 Query: '{query}'")
    print(f"📚 Input: {len(relevant_docs)} retrieved chunks")

    # Show individual chunks before combining
    print("\n📋 Individual chunks:")
    for i, doc in enumerate(relevant_docs, 1):
        page = doc.metadata.get("page", "Unknown")
        size = len(doc.page_content)
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"   {i}. Page {page} ({size} chars): {preview}...")

    # Combine chunks into enriched context
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    print("\n🎯 Enriched context created:")
    print(f"   Total length: {len(context)} characters")
    print(f"   Word count: {len(context.split())} words")
    print(f"   Combined from {len(relevant_docs)} sources")

    return context


def analyze_context_quality(context, query):
    """Analyze the quality of enriched context"""
    print("\n🔍 CONTEXT QUALITY ANALYSIS")
    print("=" * 40)

    # Basic statistics
    sentences = context.count(".") + context.count("!") + context.count("?")
    paragraphs = context.count("\n\n") + 1
    words = len(context.split())

    print("📊 Context statistics:")
    print(f"   Words: {words}")
    print(f"   Sentences: ~{sentences}")
    print(f"   Paragraphs: {paragraphs}")

    # Check for query terms
    query_words = set(query.lower().split())
    context_words = set(context.lower().split())
    matching_words = query_words.intersection(context_words)

    print("\n🔗 Query relevance:")
    print(f"   Query words in context: {len(matching_words)}/{len(query_words)}")
    if matching_words:
        print(f"   Matching terms: {', '.join(list(matching_words)[:5])}")

    # Check context coherence
    chunks_in_context = context.split("\n\n")
    unique_pages = set()

    for chunk in chunks_in_context:
        # Simple heuristic: look for page-like content patterns
        if len(chunk) > 100:
            unique_pages.add(len(chunk))  # Simplified page detection

    print("\n📄 Context coverage:")
    print(f"   Information chunks: {len(chunks_in_context)}")
    print(f"   Estimated sources: {len(unique_pages)}")

    # Quality indicators
    quality_score = 0
    indicators = []

    if words >= 200:
        quality_score += 1
        indicators.append("✅ Sufficient length")
    else:
        indicators.append("⚠️  May be too short")

    if len(matching_words) >= len(query_words) * 0.5:
        quality_score += 1
        indicators.append("✅ Good query relevance")
    else:
        indicators.append("⚠️  Low query relevance")

    if len(chunks_in_context) >= 2:
        quality_score += 1
        indicators.append("✅ Multiple perspectives")
    else:
        indicators.append("⚠️  Single source")

    print("\n🎯 Quality assessment:")
    for indicator in indicators:
        print(f"   {indicator}")

    overall_quality = ["Poor", "Fair", "Good", "Excellent"][quality_score]
    print(f"   Overall: {overall_quality} ({quality_score}/3)")


def demonstrate_context_enrichment():
    """Demonstrate context enrichment with different queries"""
    print("\n🎭 CONTEXT ENRICHMENT EXAMPLES")
    print("=" * 40)

    # Prepare vector store
    vector_store = prepare_vector_store()
    if not vector_store:
        return

    # Test different types of queries
    test_queries = [
        {"query": "What causes climate change?", "description": "Factual question"},
        {"query": "greenhouse gas emissions", "description": "Keyword search"},
        {
            "query": "How can we reduce environmental impact?",
            "description": "Solution-oriented",
        },
    ]

    for test in test_queries:
        query = test["query"]
        description = test["description"]

        print(f"\n{'=' * 20} {description.upper()} {'=' * 20}")

        # Retrieve relevant documents
        relevant_docs = vector_store.similarity_search(query, k=3)

        # Enrich context
        context = step5_enrich_context(relevant_docs, query)

        # Analyze quality
        analyze_context_quality(context, query)

        # Show context preview
        print("\n📖 Context preview:")
        print("-" * 50)
        print(context[:300] + "..." if len(context) > 300 else context)
        print("-" * 50)


def compare_context_sizes():
    """Compare different amounts of retrieved context"""
    print("\n⚖️  CONTEXT SIZE COMPARISON")
    print("=" * 40)

    vector_store = prepare_vector_store()
    if not vector_store:
        return

    query = "climate change effects"
    k_values = [1, 3, 5]

    for k in k_values:
        print(f"\n📊 Using top {k} retrieved chunks:")

        relevant_docs = vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        words = len(context.split())
        chars = len(context)

        print(f"   Context size: {chars} chars, {words} words")
        print(f"   Sources: {len(relevant_docs)} chunks")

        # Quick relevance check
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())
        relevance = len(query_words.intersection(context_words)) / len(query_words)

        print(f"   Relevance: {relevance:.1%}")


def main():
    """Demonstrate context enrichment"""
    print("🎓 RAG TUTORIAL - STEP 5: CONTEXT ENRICHMENT")
    print("=" * 60)

    try:
        # Demonstrate context enrichment
        demonstrate_context_enrichment()

        # Compare different context sizes
        compare_context_sizes()

        print("\n📚 KEY LEARNINGS:")
        print("- Context enrichment combines multiple retrieved chunks")
        print("- Quality depends on relevance and completeness")
        print("- More chunks provide broader context but may add noise")
        print("- Good context contains query-relevant information")
        print("- Context quality affects final answer quality")

        print("\n🎯 Next step: Answer Generation (step6_answer_generation.py)")

    except Exception as e:
        print(f"❌ Error in context enrichment: {e}")
        print("💡 Make sure Ollama is running and the model is available")


if __name__ == "__main__":
    main()
