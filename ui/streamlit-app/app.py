"""
Streamlit RAG Chatbot Application

This app exercises the RAG Chatbot MCP Platform by:
1. Loading sample documents
2. Chunking documents
3. Creating embeddings
4. Storing in vector database
5. Retrieving relevant chunks
6. Generating responses using Ollama
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json

# Add parent directories to path
# Resolve to absolute path to handle relative paths correctly
# app.py is at: ui/streamlit-app/app.py
# So we need to go up 3 levels: streamlit-app -> ui -> project_root
app_file = Path(__file__).resolve()
project_root = app_file.parent.parent.parent

# Verify project_root by checking for key directories
if not (project_root / "servers").exists() and (project_root.parent / "servers").exists():
    # If servers doesn't exist at this level, try one more level up
    project_root = project_root.parent

sys.path.insert(0, str(project_root))

# Import MCP server managers using importlib to handle hyphens in module names
import importlib.util

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load server modules - resolve paths to absolute
datasources_path = (project_root / "servers" / "mcp-datasources" / "src" / "server.py").resolve()
chunker_path = (project_root / "servers" / "mcp-chunker" / "src" / "server.py").resolve()
embeddings_path = (project_root / "servers" / "mcp-embeddings" / "src" / "server.py").resolve()
vectorstore_path = (project_root / "servers" / "mcp-vectorstore" / "src" / "server.py").resolve()
retriever_path = (project_root / "servers" / "mcp-retriever" / "src" / "server.py").resolve()

# Verify paths exist
for name, path in [("datasources", datasources_path), ("chunker", chunker_path), 
                   ("embeddings", embeddings_path), ("vectorstore", vectorstore_path),
                   ("retriever", retriever_path)]:
    if not path.exists():
        raise FileNotFoundError(f"Server module not found: {name} at {path}")

datasources_module = load_module_from_path("datasources_server", datasources_path)
chunker_module = load_module_from_path("chunker_server", chunker_path)
embeddings_module = load_module_from_path("embeddings_server", embeddings_path)
vectorstore_module = load_module_from_path("vectorstore_server", vectorstore_path)
retriever_module = load_module_from_path("retriever_server", retriever_path)

# Extract managers
DataSourcesManager = datasources_module.DataSourcesManager
ChunkerManager = chunker_module.ChunkerManager
EmbeddingManager = embeddings_module.EmbeddingManager
VectorStoreManager = vectorstore_module.VectorStoreManager
RetrieverManager = retriever_module.RetrieverManager

# Ollama integration
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    st.warning("⚠️ Ollama not installed. Install with: pip install ollama")

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.collection_name = "rag_documents"
    st.session_state.documents_loaded = False
    st.session_state.indexed = False
    st.session_state.chat_history = []

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot MCP",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RAG Chatbot MCP Platform")
st.markdown("Exercise the RAG pipeline with document loading, indexing, retrieval, and generation")

# Instructions
with st.expander("📖 How to Use This App", expanded=True):
    st.markdown("""
    **Follow these steps to use the RAG Chatbot:**
    
    1. **📚 Document Loading Tab:**
       - Click "📥 Load Sample Documents" to load the sample markdown files
       - Wait for the success message showing how many documents were loaded
       - Click "🔨 Index Documents" to chunk, embed, and store the documents
       - Wait for indexing to complete (this may take a minute)
    
    2. **🔍 Query & Chat Tab:**
       - Make sure Ollama is running: `ollama serve` (in a separate terminal)
       - Ensure you have a model pulled: `ollama pull llama3.2:1b` or `ollama pull tinyllama`
       - Type your question in the chat input at the bottom
       - Press Enter or click send
       - View the response and source documents
    
    3. **📊 Status Tab:**
       - Check system status and collection information
    
    **Prerequisites:**
    - Ollama must be running locally
    - A small model must be pulled (llama3.2:1b or tinyllama recommended)
    """)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    ollama_model = st.selectbox(
        "Ollama Model",
        ["llama3.2:1b", "tinyllama", "phi3:mini", "qwen2:0.5b"],
        help="Select the smallest working model for generation"
    )
    
    # Collection name
    collection_name = st.text_input(
        "Collection Name",
        value=st.session_state.collection_name,
        help="Name for the vector collection"
    )
    st.session_state.collection_name = collection_name
    
    # Embedding model
    embedding_model = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2"],
        help="Local embedding model (sentence-transformers)"
    )
    
    # Chunk size
    chunk_size = st.slider("Chunk Size", 256, 1024, 512, 64)
    chunk_overlap = st.slider("Chunk Overlap", 0, 200, 50, 10)
    st.caption("💡 Changing chunk settings requires re-indexing documents")
    
    # Retrieval parameters
    top_k = st.slider("Top K Results", 1, 10, 3)
    st.caption("💡 Top K applies to new queries (no re-indexing needed)")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📚 Document Loading", "🔍 Query & Chat", "📊 Status"])

# Tab 1: Document Loading
with tab1:
    st.header("Load and Index Documents")
    
    # Initialize managers
    if not st.session_state.initialized:
        with st.spinner("Initializing managers..."):
            try:
                st.session_state.datasource_manager = DataSourcesManager()
                # Initialize with current slider values
                st.session_state.chunker_manager = ChunkerManager(
                    default_chunk_size=chunk_size,
                    default_overlap=chunk_overlap
                )
                st.session_state.embedding_manager = EmbeddingManager(
                    default_model=embedding_model
                )
                st.session_state.vectorstore_manager = VectorStoreManager(
                    backend="chromadb",
                    persist_dir="./chroma_db",
                    chroma_host="localhost",
                    chroma_port=8000
                )
                st.session_state.retriever_manager = RetrieverManager()
                st.session_state.initialized = True
                st.success("✅ Managers initialized!")
            except Exception as e:
                st.error(f"❌ Error initializing: {e}")
                st.stop()
    
    # Update chunker manager settings if sliders changed (for re-indexing)
    if st.session_state.initialized:
        # Update chunker manager with current slider values
        st.session_state.chunker_manager.chunk_size = chunk_size
        st.session_state.chunker_manager.overlap = chunk_overlap
    
    # Load sample documents
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Load Sample Documents")
        # Use project_root that was already calculated
        sample_data_path = (project_root / "data" / "sample-data").resolve()
        
        if st.button("📥 Load Sample Documents", type="primary"):
            with st.spinner("Loading documents..."):
                try:
                    # Verify path exists
                    if not sample_data_path.exists():
                        st.error(f"❌ Sample data path not found: {sample_data_path}")
                    else:
                        result = st.session_state.datasource_manager.load_files(
                            str(sample_data_path),
                            pattern="*.md",
                            recursive=False
                        )
                    
                        if result["status"] == "success":
                            st.session_state.loaded_documents = result["documents"]
                            st.session_state.documents_loaded = True
                            st.success(f"✅ Loaded {result['count']} documents!")
                            st.json(result)
                        else:
                            st.error(f"❌ Error loading: {result.get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    
    with col2:
        st.subheader("Load Custom Documents")
        custom_path = st.text_input(
            "Path to documents",
            value=str(sample_data_path),
            help="Enter path to directory or file"
        )
        
        if st.button("📥 Load Custom Path"):
            with st.spinner("Loading..."):
                try:
                    result = st.session_state.datasource_manager.load_files(
                        custom_path,
                        pattern="*.md",
                        recursive=True
                    )
                    
                    if result["status"] == "success":
                        if "loaded_documents" not in st.session_state:
                            st.session_state.loaded_documents = []
                        st.session_state.loaded_documents.extend(result["documents"])
                        st.session_state.documents_loaded = True
                        st.success(f"✅ Loaded {result['count']} additional documents!")
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    # Index documents
    if st.session_state.documents_loaded:
        st.divider()
        st.subheader("Index Documents")
        
        if st.button("🔨 Index Documents", type="primary"):
            with st.spinner("Indexing documents..."):
                try:
                    # Step 1: Chunk documents
                    all_chunks = []
                    all_metadatas = []
                    all_ids = []
                    
                    for doc_idx, doc in enumerate(st.session_state.loaded_documents):
                        content = doc.get("content", "")
                        metadata = doc.get("metadata", {})
                        
                        # Chunk the document
                        chunk_result = st.session_state.chunker_manager.chunk_text(
                            text=content,
                            strategy="recursive",
                            chunk_size=chunk_size,
                            overlap=chunk_overlap
                        )
                        
                        chunks_data = chunk_result.get("chunks", [])
                        
                        for chunk_idx, chunk_data in enumerate(chunks_data):
                            # Extract text from chunk data structure
                            chunk_text = chunk_data.get("text", "") if isinstance(chunk_data, dict) else chunk_data
                            all_chunks.append(chunk_text)
                            all_metadatas.append({
                                **metadata,
                                "chunk_index": chunk_idx,
                                "document_index": doc_idx
                            })
                            all_ids.append(f"doc_{doc_idx}_chunk_{chunk_idx}")
                    
                    st.info(f"Created {len(all_chunks)} chunks from {len(st.session_state.loaded_documents)} documents")
                    
                    # Step 2: Create embeddings
                    embeddings = []
                    with st.spinner("Creating embeddings..."):
                        embed_result = st.session_state.embedding_manager.embed_batch(
                            texts=all_chunks,
                            model=embedding_model
                        )
                        
                        if embed_result["status"] == "success":
                            embeddings = embed_result["embeddings"]
                            st.info(f"Created {len(embeddings)} embeddings")
                        else:
                            st.error("Failed to create embeddings")
                            st.stop()
                    
                    # Step 3: Create collection and add to vectorstore
                    with st.spinner("Storing in vector database..."):
                        # Create collection
                        coll_result = st.session_state.vectorstore_manager.create_collection(
                            name=collection_name,
                            embedding_dimension=len(embeddings[0]) if embeddings else 384
                        )
                        
                        # Add documents
                        add_result = st.session_state.vectorstore_manager.add_documents(
                            collection=collection_name,
                            documents=all_chunks,
                            embeddings=embeddings,
                            metadatas=all_metadatas,
                            ids=all_ids
                        )
                        
                        if add_result["status"] == "success":
                            st.session_state.indexed = True
                            st.session_state.chunk_count = len(all_chunks)
                            st.success(f"✅ Indexed {add_result['added']} chunks!")
                        else:
                            st.error("Failed to index documents")
                    
                except Exception as e:
                    st.error(f"❌ Error indexing: {e}")
                    import traceback
                    st.code(traceback.format_exc())

# Tab 2: Query & Chat
with tab2:
    st.header("Query the RAG System")
    
    # Check prerequisites
    if not st.session_state.get("documents_loaded", False):
        st.warning("⚠️ **Step 1 Required:** Please load documents first in the 'Document Loading' tab.")
        st.info("Click '📥 Load Sample Documents' in the Document Loading tab.")
    elif not st.session_state.get("indexed", False):
        st.warning("⚠️ **Step 2 Required:** Documents are loaded but not indexed yet.")
        st.info("Go back to the 'Document Loading' tab and click '🔨 Index Documents' to continue.")
    elif not OLLAMA_AVAILABLE:
        st.error("❌ **Ollama not available:** Install with `pip install ollama`")
    else:
        # Chat interface
        st.subheader("💬 Chat")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    with st.expander("📎 Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.text(f"[{i}] {source.get('text', '')[:200]}...")
        
        # Query input
        query = st.chat_input("Ask a question about the documents...")
        
        if query:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            with st.chat_message("user"):
                st.markdown(query)
            
            # Process query
            with st.chat_message("assistant"):
                with st.spinner("Processing query..."):
                    try:
                        # Step 1: Create query embedding
                        query_embed_result = st.session_state.embedding_manager.embed_text(
                            text=query,
                            model=embedding_model
                        )
                        
                        if query_embed_result["status"] != "success":
                            st.error("Failed to create query embedding")
                            st.stop()
                        
                        query_embedding = query_embed_result["embedding"]
                        
                        # Step 2: Retrieve relevant chunks
                        try:
                            search_result = st.session_state.vectorstore_manager.search_similar(
                                collection=collection_name,
                                query_embedding=query_embedding,
                                top_k=top_k
                            )
                            
                            if search_result["status"] != "success":
                                st.error(f"Failed to retrieve documents: {search_result.get('error', 'Unknown error')}")
                                st.info("Make sure documents were indexed successfully. Check the Status tab.")
                                st.stop()
                            
                            retrieved_docs = search_result.get("results", [])
                            
                            if not retrieved_docs:
                                st.warning("No documents retrieved. Try re-indexing your documents.")
                                st.stop()
                        except Exception as e:
                            st.error(f"Error retrieving documents: {e}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
                            st.stop()
                        
                        # Step 3: Format context
                        context_docs = []
                        for doc in retrieved_docs:
                            context_docs.append({
                                "text": doc.get("document", ""),
                                "metadata": doc.get("metadata", {})
                            })
                        
                        # Step 4: Generate response with Ollama
                        if not OLLAMA_AVAILABLE:
                            st.error("Ollama not available. Install with: pip install ollama")
                            response_text = "Ollama is required for generation."
                        else:
                            # Format prompt
                            context_str = "\n\n".join([
                                f"[{i+1}] {doc['text']}" 
                                for i, doc in enumerate(context_docs)
                            ])
                            
                            prompt = f"""Based on the following context, answer the question.

Context:
{context_str}

Question: {query}

Answer:"""
                            
                            # Call Ollama
                            try:
                                ollama_response = ollama.generate(
                                    model=ollama_model,
                                    prompt=prompt
                                )
                                response_text = ollama_response["response"]
                            except Exception as e:
                                error_msg = str(e)
                                st.error(f"❌ Ollama error: {error_msg}")
                                if "connection" in error_msg.lower() or "refused" in error_msg.lower():
                                    st.info("💡 **Tip:** Make sure Ollama is running. Start it with: `ollama serve`")
                                elif "model" in error_msg.lower() and "not found" in error_msg.lower():
                                    st.info(f"💡 **Tip:** Pull the model first: `ollama pull {ollama_model}`")
                                response_text = f"Error generating response: {error_msg}"
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                        
                        # Display response
                        st.markdown(response_text)
                        
                        # Display sources
                        with st.expander("📎 Sources"):
                            for i, doc in enumerate(retrieved_docs, 1):
                                st.text(f"[{i}] Score: {doc.get('distance', 0):.3f}")
                                st.text(doc.get("document", "")[:300] + "...")
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response_text,
                            "sources": retrieved_docs
                        })
                        
                    except Exception as e:
                        error_msg = f"Error processing query: {e}"
                        st.error(error_msg)
                        import traceback
                        st.code(traceback.format_exc())

# Tab 3: Status
with tab3:
    st.header("System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initialized", "✅" if st.session_state.initialized else "❌")
        st.metric("Documents Loaded", 
                 len(st.session_state.loaded_documents) if st.session_state.documents_loaded else 0)
    
    with col2:
        st.metric("Indexed", "✅" if st.session_state.indexed else "❌")
        st.metric("Chunks Indexed", 
                 st.session_state.chunk_count if st.session_state.indexed else 0)
    
    with col3:
        st.metric("Ollama Available", "✅" if OLLAMA_AVAILABLE else "❌")
        st.metric("Chat Messages", len(st.session_state.chat_history))
    
    # Collection info
    if st.session_state.indexed:
        st.divider()
        st.subheader("Collection Information")
        
        try:
            stats = st.session_state.vectorstore_manager.get_collection_stats(
                collection=collection_name
            )
            st.json(stats)
        except Exception as e:
            st.error(f"Error getting stats: {e}")
    
    # Clear chat button
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

