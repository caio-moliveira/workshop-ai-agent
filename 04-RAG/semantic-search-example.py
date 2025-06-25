#!/usr/bin/env python3
"""
RAG Step 4: Semantic Search
Learn how to find relevant information using vector similarity
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
    """Prepare vector store for search demonstration"""
    pdf_path = "04-RAG/data/Understanding_Climate_Change.pdf"

    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return None, None

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

    return vector_store, embeddings


def step4_semantic_search(vector_store, query, k=3):
    """
    Step 4: Semantic Search

    This step demonstrates:
    - How semantic search works
    - Finding relevant documents by meaning
    - Ranking results by similarity
    - Different search parameters
    """
    print("🔍 STEP 4: Semantic Search")
    print("=" * 40)

    print(f"🔎 Search query: '{query}'")
    print(f"🎯 Retrieving top {k} most similar chunks")

    # Perform similarity search
    relevant_docs = vector_store.similarity_search(query, k=k)

    print(f"\n✅ Found {len(relevant_docs)} relevant chunks")

    # Display results
    for i, doc in enumerate(relevant_docs, 1):
        print(f"\n--- Result {i} ---")
        print(f"📄 Source: Page {doc.metadata.get('page', 'Unknown')}")
        print(f"📝 Content length: {len(doc.page_content)} characters")
        print("📖 Content preview:")
        print(f"   {doc.page_content[:300]}...")

        # Show why this might be relevant
        query_words = set(query.lower().split())
        content_words = set(doc.page_content.lower().split())
        common_words = query_words.intersection(content_words)

        if common_words:
            print(f"🔗 Common keywords: {', '.join(list(common_words)[:5])}")

    return relevant_docs


def compare_search_methods(vector_store):
    """Compare semantic search vs keyword search"""
    print("\n⚖️  SEMANTIC VS KEYWORD SEARCH")
    print("=" * 40)

    # Test queries that show the difference
    test_cases = [
        {"query": "greenhouse effect", "description": "Direct keyword match"},
        {
            "query": "warming planet",
            "description": "Semantic similarity (no exact match)",
        },
        {"query": "CO2 emissions", "description": "Technical terms"},
        {"query": "environmental impact", "description": "Related concepts"},
    ]

    for case in test_cases:
        query = case["query"]
        description = case["description"]

        print(f"\n🔍 Query: '{query}' ({description})")

        # Semantic search
        semantic_results = vector_store.similarity_search(query, k=2)

        print(f"📊 Semantic search found {len(semantic_results)} results:")
        for i, doc in enumerate(semantic_results, 1):
            # Extract first sentence for preview
            first_sentence = doc.page_content.split(".")[0][:100]
            print(f"   {i}. {first_sentence}...")

        # Simple keyword search simulation
        all_docs = vector_store.similarity_search("", k=1000)  # Get all docs
        keyword_matches = []

        for doc in all_docs:
            if any(word.lower() in doc.page_content.lower() for word in query.split()):
                keyword_matches.append(doc)
                if len(keyword_matches) >= 2:
                    break

        print(f"🔤 Keyword search found {len(keyword_matches)} exact matches:")
        for i, doc in enumerate(keyword_matches, 1):
            first_sentence = doc.page_content.split(".")[0][:100]
            print(f"   {i}. {first_sentence}...")


def demonstrate_search_parameters(vector_store):
    """Demonstrate different search parameters"""
    print("\n⚙️  SEARCH PARAMETERS")
    print("=" * 40)

    query = "climate change causes"

    # Test different k values
    k_values = [1, 3, 5]

    for k in k_values:
        print(f"\n📊 Retrieving top {k} results:")
        results = vector_store.similarity_search(query, k=k)

        for i, doc in enumerate(results, 1):
            relevance_indicator = "🟢" if i <= 2 else "🟡" if i <= 4 else "🔴"
            first_line = doc.page_content.split("\n")[0][:80]
            print(f"   {relevance_indicator} {i}. {first_line}...")


def similarity_scores_demo(vector_store, embeddings):
    """Demonstrate similarity scores"""
    print("\n📊 SIMILARITY SCORES DEMONSTRATION")
    print("=" * 40)

    query = "renewable energy sources"

    # Get results with scores
    results_with_scores = vector_store.similarity_search_with_score(query, k=5)

    print(f"🔍 Query: '{query}'")
    print("📈 Results with similarity scores (lower = more similar):")

    for i, (doc, score) in enumerate(results_with_scores, 1):
        # Determine relevance level
        if score < 0.5:
            relevance = "🟢 High"
        elif score < 0.8:
            relevance = "🟡 Medium"
        else:
            relevance = "🔴 Low"

        first_sentence = doc.page_content.split(".")[0][:100]
        print(f"\n   {i}. Score: {score:.4f} {relevance}")
        print(f"      {first_sentence}...")


def interactive_search(vector_store):
    """Interactive search demonstration"""
    print("\n🎮 INTERACTIVE SEARCH")
    print("=" * 40)

    sample_queries = [
        "What causes global warming?",
        "Effects of climate change",
        "How to reduce carbon emissions?",
        "Renewable energy benefits",
    ]

    print("💡 Try these sample queries or enter your own:")
    for i, query in enumerate(sample_queries, 1):
        print(f"   {i}. {query}")

    while True:
        user_query = input("\n🔍 Enter search query (or 'quit' to exit): ").strip()

        if user_query.lower() in ["quit", "exit", "q"]:
            break

        if not user_query:
            continue

        print(f"\n🔎 Searching for: '{user_query}'")
        results = vector_store.similarity_search(user_query, k=2)

        for i, doc in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"📄 Page: {doc.metadata.get('page', 'Unknown')}")
            print(f"📝 Content: {doc.page_content[:200]}...")


def main():
    """Demonstrate semantic search"""
    print("🎓 RAG TUTORIAL - STEP 4: SEMANTIC SEARCH")
    print("=" * 60)

    try:
        # Prepare vector store
        print("📦 Preparing vector store...")
        vector_store, embeddings = prepare_vector_store()

        if not vector_store:
            return

        print("✅ Vector store ready")

        # Basic semantic search
        query = "What is the main cause of climate change?"
        relevant_docs = step4_semantic_search(vector_store, query, k=3)

        # Compare search methods
        compare_search_methods(vector_store)

        # Demonstrate parameters
        demonstrate_search_parameters(vector_store)

        # Show similarity scores
        similarity_scores_demo(vector_store, embeddings)

        # Interactive search
        interactive_search(vector_store)

        print("\n📚 KEY LEARNINGS:")
        print("- Semantic search finds meaning, not just keywords")
        print("- Vector similarity measures conceptual closeness")
        print("- k parameter controls number of results")
        print("- Lower similarity scores mean higher relevance")
        print("- Semantic search handles synonyms and related concepts")
        print("- Results are ranked by relevance automatically")

        print("\n🎯 Next step: Context Enrichment (step5_context_enrichment.py)")

    except Exception as e:
        print(f"❌ Error in semantic search: {e}")
        print("💡 Make sure Ollama is running and the model is available")


if __name__ == "__main__":
    main()
