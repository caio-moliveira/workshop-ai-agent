# ================================
# SIMPLE SEMANTIC SEARCH EXAMPLE
# ================================

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# ================================
# EXAMPLE 1: Connect to Vector Database
# ================================

cur_dir = os.getcwd()
vdb_dir = os.path.join(cur_dir, "04-RAG", "db", "climate_vectorstore")

print("=== CONNECTING TO VECTOR DATABASE ===")
print(f"Database directory: {vdb_dir}")

# Initialize embeddings model - Choose one:

# Option 1: OpenAI embeddings
# embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Option 2: Ollama embeddings (comment/uncomment to switch)
embeddings_model = OllamaEmbeddings(model="mxbai-embed-large:latest")

# Connect to existing vector database
db = Chroma(persist_directory=vdb_dir, embedding_function=embeddings_model)

print(f"Model being used: {type(embeddings_model).__name__}")
print("✅ Connected to vector database!")

# ================================
# EXAMPLE 2: Simple Query
# ================================

query = "What is the main cause of climate change?"

print("\n=== SEMANTIC SEARCH ===")
print(f"Query: '{query}'")

# Retrieve relevant documents based on the query
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

relevant_chunks = retriever.invoke(query)

print(f"Found {len(relevant_chunks)} relevant chunks")
print(f"Type of result: {type(relevant_chunks)}")

# ================================
# EXAMPLE 3: Display Results
# ================================

print("\n=== SEARCH RESULTS ===")

for i, chunk in enumerate(relevant_chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(f"Content: {chunk.page_content}")
    print(f"Type: {type(chunk)}")

    if chunk.metadata:
        print(f"Metadata: {chunk.metadata}")
    print("-" * 50)

# ================================
# EXAMPLE 4: Different Search Types
# ================================

print("\n=== DIFFERENT SEARCH METHODS ===")

# Method 1: Basic similarity
basic_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
basic_results = basic_retriever.invoke(query)

print(f"Basic similarity: {len(basic_results)} results")

# Method 2: With score threshold
score_retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.3},
)
score_results = score_retriever.invoke(query)

print(f"With score threshold: {len(score_results)} results")


# ================================
# EXAMPLE 6: Show Similarity in Action
# ================================

print("\n=== SEMANTIC SIMILARITY DEMO ===")

# Similar queries should return similar results
query1 = "What causes climate change?"
query2 = "What are the reasons for global warming?"
query3 = "What is the weather like today?"

results1 = retriever.invoke(query1)
results2 = retriever.invoke(query2)
results3 = retriever.invoke(query3)

print(f"Query 1: '{query1}' → {len(results1)} results")
print(f"Query 2: '{query2}' → {len(results2)} results")
print(f"Query 3: '{query3}' → {len(results3)} results")

print("\nNotice: Similar queries (1&2) find relevant climate info")
print("Different queries (3) might find less relevant results")

# ================================
# EXAMPLE 7: What's Happening Behind the Scenes
# ================================

print("\n=== WHAT'S HAPPENING BEHIND THE SCENES ===")
print("1. Your query gets converted to an embedding vector")
print("2. Database compares your vector to all stored chunk vectors")
print("3. Finds chunks with most similar vectors (closest meaning)")
print("4. Returns the most relevant chunks")
print("5. This is called 'semantic search' - search by meaning!")
