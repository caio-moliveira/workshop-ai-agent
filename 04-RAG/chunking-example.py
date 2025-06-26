# ================================
# CHUNKING: CHARACTERS VS TOKENS
# ================================

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import tiktoken

# Initialize tokenizer for counting tokens
tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-3.5/4 tokenizer


def count_tokens(text):
    return len(tokenizer.encode(text))


# ================================
# EXAMPLE 1: Character-based Chunking (Default)
# ================================

loader = PyPDFLoader("04-RAG/data/Understanding_Climate_Change.pdf")
docs = loader.load()

# Default splitter - splits by paragraphs (\n\n)
default_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
default_chunks = default_splitter.split_documents(docs)

print("=== DEFAULT SPLITTER (separator='\\n\\n') ===")
print("This splits by PARAGRAPHS, not by exact character count!")
print("Chunk size setting: 1000 characters")
print(f"Number of chunks: {len(default_chunks)}")

chunk_sizes = [len(chunk.page_content) for chunk in default_chunks]
token_counts = [count_tokens(chunk.page_content) for chunk in default_chunks]

print(f"Actual chunk sizes (chars): {chunk_sizes[:5]}...")
print(f"Actual chunk sizes (tokens): {token_counts[:5]}...")
print(f"Average size: {sum(chunk_sizes) / len(chunk_sizes):.0f} characters")
print(f"Average tokens: {sum(token_counts) / len(token_counts):.0f} tokens")

# ================================
# EXAMPLE 2: How It Actually Works
# ================================

print("\n=== HOW IT WORKS ===")
print("1. Split text by separator (\\n\\n by default)")
print("2. Group paragraphs until reaching ~1000 characters")
print("3. If a single paragraph > 1000 chars, keep it whole")
print("4. That's why chunks can be much larger than 1000!")

# Show first chunk content
print(
    f"\nFirst chunk ({len(default_chunks[0].page_content)} chars, {count_tokens(default_chunks[0].page_content)} tokens):"
)
print(default_chunks[0].page_content[:300] + "...")

# ================================
# EXAMPLE 3: Different Separators
# ================================

# Split by single newlines (sentences/lines)
line_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=0)
line_chunks = line_splitter.split_documents(docs)

# Split by periods (sentences)
sentence_splitter = CharacterTextSplitter(
    separator=". ", chunk_size=1000, chunk_overlap=0
)
sentence_chunks = sentence_splitter.split_documents(docs)

print("\n=== DIFFERENT SEPARATORS ===")
print(f"By paragraphs (\\n\\n): {len(default_chunks)} chunks")
print(f"By lines (\\n): {len(line_chunks)} chunks")
print(f"By sentences ('. '): {len(sentence_chunks)} chunks")

# ================================
# EXAMPLE 4: Force Split at Exact Size
# ================================

# This will split at EXACTLY 1000 characters
exact_splitter = CharacterTextSplitter(
    separator="",  # Split by individual characters
    chunk_size=1000,
    chunk_overlap=0,
)
exact_chunks = exact_splitter.split_documents(docs)

print("\n=== EXACT CHARACTER SPLITTING ===")
print("Using separator='' forces exact character count")
print(f"Number of chunks: {len(exact_chunks)}")

exact_sizes = [len(chunk.page_content) for chunk in exact_chunks]
print(f"Chunk sizes: {exact_sizes[:5]}...")
print("Notice: All chunks are exactly 1000 characters (except last)")

# ================================
# EXAMPLE 5: What Happens with Large Paragraphs
# ================================

print("\n=== LARGE PARAGRAPH EXAMPLE ===")

# Create a sample document with one very long paragraph
sample_text = "This is a very long paragraph. " * 100  # ~3000 characters
sample_doc = type("Document", (), {"page_content": sample_text, "metadata": {}})()

# Try to split it
para_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000)
para_result = para_splitter.split_documents([sample_doc])

print(f"Original text: {len(sample_text)} characters")
print("Chunk size setting: 1000 characters")
print(f"Result: {len(para_result)} chunk(s)")
print(f"Actual chunk size: {len(para_result[0].page_content)} characters")
print("Reason: No \\n\\n found, so entire text becomes one chunk!")

# ================================
# EXAMPLE 6: Pages vs Chunks
# ================================

print("\n=== PAGES VS CHUNKS ===")
print(f"PDF pages loaded: {len(docs)}")
print(f"Chunks created: {len(default_chunks)}")
print(f"Ratio: {len(default_chunks) / len(docs):.1f} chunks per page")

# Show which page each chunk comes from
print("\nChunk sources:")
for i, chunk in enumerate(default_chunks[:5]):
    page_num = chunk.metadata.get("page", "Unknown")
    char_count = len(chunk.page_content)
    token_count = count_tokens(chunk.page_content)
    print(
        f"Chunk {i + 1}: Page {page_num}, {char_count} characters, {token_count} tokens"
    )

# ================================
# SUMMARY
# ================================

print("\n=== SUMMARY ===")
print("CharacterTextSplitter does NOT split at exact character count!")
print("It splits by separator first, then groups to reach target size")
print("Default separator is '\\n\\n' (paragraphs)")
print("If you want exact 1000-character chunks, use separator=''")
print("But this might break sentences/words!")
print(f"Token ratio: ~{sum(chunk_sizes) / sum(token_counts):.1f} characters per token")
