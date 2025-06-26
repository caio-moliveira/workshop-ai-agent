# ================================
# SIMPLE EMBEDDINGS EXAMPLE
# ================================

from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings


# ================================
# EXAMPLE 1: Basic Embeddings
# ================================

# Initialize embeddings model - Choose one:

# Option 1: OpenAI embeddings
# embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Option 2: Ollama embeddings (comment/uncomment to switch)
embeddings_model = OllamaEmbeddings(model="mxbai-embed-large:latest")


# ================================
# EXAMPLE: Chunk Embedding
# ================================

# Use a sample chunk text
chunk_text = (
    "Climate change refers to significant, long-term changes in the global climate"
)

print("\n=== CHUNK EMBEDDING ===")
print(f"Chunk text: '{chunk_text}'")
print(f"Chunk text length: {len(chunk_text)} characters")

# Embed the chunk
chunk_embedding = embeddings_model.embed_documents([chunk_text])

print("\nEmbedding result:")
print(f"Type: {type(chunk_embedding)}")
print(f"Number of embeddings: {len(chunk_embedding)}")
print(f"Vector dimensions: {len(chunk_embedding[0])}")

# ================================
# EXAMPLE: Show Chunk Vector Numbers
# ================================

print("\n=== CHUNK VECTOR NUMBERS ===")
vector = chunk_embedding[0]

print(f"Full vector length: {len(vector)}")
print(f"First 20 numbers: {vector[:20]}")
print(f"Middle 20 numbers: {vector[750:770]}")
print(f"Last 20 numbers: {vector[-20:]}")


# ================================
# EXAMPLE: Compare Different Texts
# ================================

print("\n=== COMPARE DIFFERENT TEXTS ===")

# Use different climate-related sentences
test_texts = [
    "Climate change refers to significant, long-term changes in the global climate",
    "Global warming is causing ice caps to melt rapidly",
    "The weather today is sunny and warm",
]

test_embeddings = embeddings_model.embed_documents(test_texts)

for i, text in enumerate(test_texts):
    vector = test_embeddings[i]
    print(f"\nText {i + 1}: {text}")
    print(f"Vector first 10: {vector[:10]}")
    print(f"Vector sum: {sum(vector):.6f}")

# ================================
# EXAMPLE: What Embeddings Represent
# ================================

print("\n=== WHAT DO THESE NUMBERS MEAN? ===")
print("Each number represents a 'feature' or 'dimension'")
print("Similar texts will have similar numbers")
if len(vector) == 1536:
    print("1536 dimensions capture different aspects of meaning (OpenAI)")
elif len(vector) == 1024:
    print("1024 dimensions capture different aspects of meaning (Ollama)")
else:
    print(f"{len(vector)} dimensions capture different aspects of meaning")
print("Positive/negative values show presence/absence of features")
print("These vectors allow computers to 'understand' text similarity")

# ================================
# SIMPLE SIMILARITY CHECK
# ================================

print("\n=== SIMPLE SIMILARITY ===")

# Compare two simple words
word1 = "climate"
word2 = "weather"
word3 = "banana"

word_embeddings = embeddings_model.embed_documents([word1, word2, word3])

print(f"'{word1}' first 10: {word_embeddings[0][:10]}")
print(f"'{word2}' first 10: {word_embeddings[1][:10]}")
print(f"'{word3}' first 10: {word_embeddings[2][:10]}")

print("\nNotice: Similar words (climate/weather) have more similar numbers")
print("than different words (climate/banana)")
