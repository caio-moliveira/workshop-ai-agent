# ================================
# SIMPLE FAISS CONTEXT ENRICHMENT
# ================================

from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# ================================
# EXAMPLE 1: Create FAISS Vector Store
# ================================

print("=== CREATING FAISS VECTOR STORE ===")

# Initialize embeddings model - Choose one:

# Option 1: OpenAI embeddings
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Option 2: Ollama embeddings (comment/uncomment to switch)
# embeddings_model = OllamaEmbeddings(model="mxbai-embed-large:latest")

# Load and chunk documents
loader = PyPDFLoader("04-RAG/data/Understanding_Climate_Change.pdf")
docs = loader.load()

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

print(f"Model being used: {type(embeddings_model).__name__}")
print(f"Number of chunks: {len(chunks)}")

# Create FAISS vector store
faiss_db = FAISS.from_documents(chunks, embeddings_model)

print("✅ FAISS vector store created!")

# ================================
# EXAMPLE 2: Basic Search
# ================================

query = "What causes climate change?"

print("\n=== BASIC SEARCH ===")
print(f"Query: '{query}'")

# Get top 3 most similar chunks
basic_results = faiss_db.similarity_search(query, k=3)

print(f"Found {len(basic_results)} chunks")
for i, chunk in enumerate(basic_results, 1):
    print(f"\nChunk {i}:")
    print(f"Content: {chunk.page_content[:150]}...")

# ================================
# EXAMPLE 3: Search with Scores
# ================================

print("\n=== SEARCH WITH SIMILARITY SCORES ===")

# Get results with similarity scores
results_with_scores = faiss_db.similarity_search_with_score(query, k=3)

print(f"Query: '{query}'")
for i, (chunk, score) in enumerate(results_with_scores, 1):
    print(f"\nResult {i} (Score: {score:.4f}):")
    print(f"Content: {chunk.page_content[:150]}...")
    print(f"Similarity: {1 - score:.4f}")  # Convert distance to similarity

# ================================
# EXAMPLE 4: Context Enrichment
# ================================

print("\n=== CONTEXT ENRICHMENT ===")

# Get more chunks for richer context
enriched_results = faiss_db.similarity_search(query, k=5)

print("Basic retrieval: 3 chunks")
print(f"Enriched retrieval: {len(enriched_results)} chunks")

print("\nEnriched context:")
for i, chunk in enumerate(enriched_results, 1):
    print(f"Chunk {i}: {chunk.page_content[:100]}...")

# ================================
# EXAMPLE 5: Different Search Parameters
# ================================

print("\n=== DIFFERENT SEARCH PARAMETERS ===")

# Conservative search (fewer, more relevant results)
conservative = faiss_db.similarity_search(query, k=2)

# Aggressive search (more results, potentially less relevant)
aggressive = faiss_db.similarity_search(query, k=8)

print(f"Conservative search (k=2): {len(conservative)} results")
print(f"Aggressive search (k=8): {len(aggressive)} results")

# ================================
# EXAMPLE 6: Multiple Query Approach
# ================================

print("\n=== MULTIPLE QUERY APPROACH ===")

# Generate related queries for better context
related_queries = [
    "What causes climate change?",
    "How do greenhouse gases contribute to global warming?",
    "What are the main drivers of climate change?",
]

all_chunks = []
for related_query in related_queries:
    results = faiss_db.similarity_search(related_query, k=2)
    all_chunks.extend(results)

# Remove duplicates (simple approach)
unique_chunks = []
seen_content = set()
for chunk in all_chunks:
    content_preview = chunk.page_content[:100]
    if content_preview not in seen_content:
        unique_chunks.append(chunk)
        seen_content.add(content_preview)

print("Single query results: 3 chunks")
print(f"Multiple query results: {len(unique_chunks)} unique chunks")

# ================================
# EXAMPLE 7: Save and Load FAISS Index
# ================================

print("\n=== SAVE AND LOAD FAISS INDEX ===")

# Save FAISS index to disk
faiss_db.save_local("04-RAG/db/faiss_index")
print("✅ FAISS index saved to disk")

# Load FAISS index from disk
loaded_faiss_db = FAISS.load_local(
    "04-RAG/db/faiss_index", embeddings_model, allow_dangerous_deserialization=True
)
print("✅ FAISS index loaded from disk")

# Test loaded index
test_results = loaded_faiss_db.similarity_search("climate change effects", k=2)
print(f"Loaded index test: {len(test_results)} results found")

# ================================
# EXAMPLE 8: FAISS vs ChromaDB Comparison
# ================================

print("\n=== FAISS ADVANTAGES ===")
print("✅ Faster similarity search")
print("✅ Better for large datasets")
print("✅ More search algorithms available")
print("✅ Can handle millions of vectors efficiently")
print("✅ Easy to save/load indexes")
print("✅ Good for context enrichment with many results")

print("\nUse FAISS when:")
print("- You need fast retrieval")
print("- Working with large document collections")
print("- Want to experiment with different search parameters")
print("- Need to enrich context with many similar chunks")
