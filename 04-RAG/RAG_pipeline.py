import os
from dotenv import load_dotenv

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.retrievers.multi_query import MultiQueryRetriever

# Load environment variables
load_dotenv()

# ================================
# STEP 1: DOCUMENT LOADING
# ================================


def load_climate_document():
    """Load the climate change PDF document"""
    print("📄 Loading climate change document...")

    # Set up file path
    cur_dir = os.getcwd()
    file_path = os.path.join(
        cur_dir, "04-RAG", "data", "understanding_climate_change.pdf"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at {file_path}")

    # Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    print(f"✅ Loaded {len(documents)} pages from the document")
    return documents


# ================================
# STEP 2: TEXT SPLITTING
# ================================


def split_documents(documents):
    """Split documents into smaller chunks for better retrieval"""
    print("✂️ Splitting documents into chunks...")

    # Create text splitter - separates by chapters and topics
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Size of each chunk
        chunk_overlap=200,  # Overlap between chunks to maintain context
        separators=[  # Split by these separators in order
            "\n\nChapter",  # Split by chapters first
            "\n\n",  # Then by paragraphs
            "\n",  # Then by lines
            " ",  # Finally by spaces
            "",
        ],
        add_start_index=True,  # Track where chunks come from
    )

    chunks = text_splitter.split_documents(documents)

    print(f"✅ Created {len(chunks)} chunks")
    print(
        f"📊 Average chunk size: {sum(len(chunk.page_content) for chunk in chunks) // len(chunks)} characters"
    )

    return chunks


# ================================
# STEP 3: EMBEDDINGS & VECTOR STORE
# ================================


def create_vector_store(chunks):
    """Create embeddings and store in vector database"""
    print("🔢 Creating embeddings and vector store...")

    # Initialize embeddings model
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

    # Set up vector store directory
    cur_dir = os.getcwd()
    vdb_dir = os.path.join(cur_dir, "04-RAG", "db", "climate_vectorstore")

    # Create vector store
    if not os.path.exists(vdb_dir):
        print("Creating new vector store...")
        vectorstore = Chroma.from_documents(
            documents=chunks, embedding=embeddings_model, persist_directory=vdb_dir
        )
    else:
        print("Loading existing vector store...")
        vectorstore = Chroma(
            persist_directory=vdb_dir, embedding_function=embeddings_model
        )

    print("✅ Vector store ready!")
    return vectorstore


# ================================
# STEP 4: RETRIEVAL SETUP
# ================================


def setup_retriever(vectorstore):
    """Set up the retriever with multiple query generation"""
    print("🔍 Setting up retriever...")

    # Initialize LLM for query generation
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Create base retriever
    base_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},  # Retrieve top 5 most similar chunks
    )

    # Wrap with MultiQueryRetriever for better results
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    print("✅ Retriever ready!")
    return retriever


# ================================
# STEP 5: ANSWER GENERATION
# ================================


def generate_answer(query, retriever):
    """Generate answer using retrieved context"""
    print(f"❓ Processing query: {query}")

    # Retrieve relevant documents
    print("🔍 Retrieving relevant information...")
    relevant_docs = retriever.invoke(query)

    # Prepare context from retrieved documents
    context = "\n\n".join(
        [f"Source {i + 1}:\n{doc.page_content}" for i, doc in enumerate(relevant_docs)]
    )

    # Create prompt
    system_prompt = """You are a helpful climate science expert. Use the provided context to answer questions about climate change.

Instructions:
- Base your answer only on the provided context
- If the answer isn't in the context, say "I don't have enough information to answer that question"
- Provide clear, educational explanations
- Include relevant details and examples when available
- Structure your answer logically

Context:
{context}
"""

    user_prompt = f"Question: {query}"

    # Generate answer
    print("🤖 Generating answer...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    messages = [
        SystemMessage(content=system_prompt.format(context=context)),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    print("✅ Answer generated!")
    return response.content, relevant_docs


# ================================
# STEP 6: SIMPLE RAG PIPELINE
# ================================


def build_rag_system():
    """Build the complete RAG system"""
    print("🚀 Building Climate Change RAG System...")
    print("=" * 50)

    # Step 1: Load documents
    documents = load_climate_document()

    # Step 2: Split into chunks
    chunks = split_documents(documents)

    # Step 3: Create vector store
    vectorstore = create_vector_store(chunks)

    # Step 4: Setup retriever
    retriever = setup_retriever(vectorstore)

    print("=" * 50)
    print("🎉 RAG System Ready!")

    return retriever


def ask_question(retriever, query):
    """Ask a question to the RAG system"""
    print("\n" + "=" * 50)

    # Generate answer
    answer, sources = generate_answer(query, retriever)

    # Display results
    print(f"\n❓ QUESTION: {query}")
    print(f"\n💡 ANSWER:\n{answer}")

    print(f"\n📚 SOURCES USED ({len(sources)} documents):")
    for i, doc in enumerate(sources[:3], 1):  # Show first 3 sources
        print(f"\nSource {i}:")
        print(f"Content preview: {doc.page_content[:200]}...")
        if "page" in doc.metadata:
            print(f"Page: {doc.metadata['page']}")

    print("=" * 50)
    return answer


# ================================
# EXAMPLE USAGE
# ================================

if __name__ == "__main__":
    # Build the RAG system
    retriever = build_rag_system()

    # Example questions about climate change
    sample_questions = [
        "What is climate change?",
        "What are the main causes of climate change?",
        "How does climate change affect ocean acidification?",
        "What are some renewable energy solutions?",
        "How can technology help with climate change mitigation?",
    ]

    print("\n🎓 DEMO: Asking sample questions...")

    # Ask a sample question
    sample_query = sample_questions[0]
    answer = ask_question(retriever, sample_query)

    print("\n" + "🔄" * 20)
    print("Try asking your own questions using:")
    print("answer = ask_question(retriever, 'Your question here')")
    print("🔄" * 20)

# ================================
# INTERACTIVE FUNCTION
# ================================


def interactive_chat(retriever):
    """Interactive chat function for students to try"""
    print("\n🤖 Climate Change RAG Chat")
    print("Ask me anything about climate change! Type 'quit' to exit.")
    print("-" * 50)

    while True:
        user_input = input("\nYour question: ").strip()

        if user_input.lower() in ["quit", "exit", "stop"]:
            print("👋 Thanks for using the Climate Change RAG system!")
            break

        if user_input:
            ask_question(retriever, user_input)
        else:
            print("Please enter a question.")


# To run interactive chat:
interactive_chat(retriever)
