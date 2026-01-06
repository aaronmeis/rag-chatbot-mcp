# Frequently Asked Questions

## General Questions

### What is the RAG Chatbot MCP Platform?
The RAG Chatbot MCP Platform is a modular system for building retrieval-augmented generation chatbots using the Model Context Protocol (MCP). It provides seven specialized servers that handle different aspects of the RAG pipeline.

### Who should use this platform?
- **AI/ML Engineers** building production RAG systems
- **Developers** exploring MCP and agentic AI
- **Researchers** experimenting with retrieval techniques
- **Students** learning about RAG architecture

### What are the system requirements?
- Python 3.10 or higher
- 8GB RAM minimum (16GB recommended)
- GPU optional but recommended for local embeddings
- API keys for OpenAI (optional, for cloud models)

## Installation Questions

### How do I install the platform?
1. Clone the repository
2. Run `./tests/manual_testing/Solution-Testing/install_dependencies.sh`
3. Configure your environment variables
4. Verify with `./tests/manual_testing/Solution-Testing/verify_servers.sh`

### Do I need an OpenAI API key?
No, the platform supports local models through Sentence Transformers. However, OpenAI models often provide better quality embeddings and generations.

### Can I use the platform offline?
Yes! Configure local models for embeddings and use Ollama or similar for generation. The mcp-embeddings server supports all-MiniLM-L6-v2 locally.

## Technical Questions

### What vector databases are supported?
- ChromaDB (default, recommended for development)
- FAISS (recommended for production)
- Additional backends can be added through the plugin system

### How do I add my own documents?
Use the mcp-datasources server to load documents:
1. Place files in the data/sample-data directory
2. Call the `load_files` tool with the directory path
3. The chunker and embeddings servers will process them automatically

### What file formats are supported?
- PDF (.pdf)
- Word documents (.docx)
- Markdown (.md)
- Plain text (.txt)
- HTML (.html)
- JSON (.json)
- CSV (.csv)

### How do I tune retrieval quality?
1. Adjust chunk size in mcp-chunker (default: 512 tokens)
2. Experiment with overlap (default: 50 tokens)
3. Enable hybrid search in mcp-retriever
4. Add reranking with mcp-reranker for better relevance

## Troubleshooting

### The servers won't start
1. Check Python version: `python3 --version` (need 3.10+)
2. Verify dependencies: `pip list | grep mcp`
3. Check logs in the terminal for specific errors

### Retrieval returns irrelevant results
1. Ensure documents are properly chunked (not too large)
2. Try different embedding models
3. Enable reranking for better relevance
4. Check if the query needs reformulation

### Generation is slow
1. Consider using a smaller/faster model
2. Reduce the number of retrieved chunks (k parameter)
3. Enable streaming for perceived faster responses
4. Check your network connection for API calls

### Out of memory errors
1. Reduce batch sizes in embedding generation
2. Use a smaller local model
3. Process documents in smaller batches
4. Increase system swap space

## Best Practices

### How should I structure my knowledge base?
- Organize documents by topic or category
- Include clear headings and sections
- Remove redundant or outdated information
- Add metadata for filtering

### What chunk size should I use?
- Start with 512 tokens for general use
- Use larger chunks (1024+) for complex topics
- Use smaller chunks (256) for Q&A style content
- Always include overlap (10-20%)

### How do I evaluate my RAG system?
1. Create a test set of questions with known answers
2. Measure retrieval precision and recall
3. Evaluate answer quality with LLM judges
4. Track latency and cost metrics
