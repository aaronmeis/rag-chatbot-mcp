# Acknowledgments

## Project Inspiration

This project structure is inspired by the excellent [precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) project by Lynn Langit, which demonstrates best practices for building modular MCP server architectures for complex domain-specific applications.

## Core Technologies

### Model Context Protocol (MCP)
- **Anthropic** - For creating and maintaining the [Model Context Protocol](https://modelcontextprotocol.io/) specification
- **MCP SDK** - Python and TypeScript SDKs for building MCP servers

### Vector Databases & Embeddings
- **ChromaDB** - Open-source embedding database
- **FAISS** - Facebook AI Similarity Search library
- **OpenAI** - Embedding models (text-embedding-ada-002, text-embedding-3-small)
- **Sentence Transformers** - Local embedding models

### RAG Components
- **LangChain** - Document loaders and text splitters
- **LlamaIndex** - RAG framework concepts
- **Haystack** - Pipeline architecture inspiration

### Development Tools
- **pytest** - Testing framework
- **FastAPI** - Async server patterns
- **Pydantic** - Data validation

## Research & Publications

### RAG Architecture
- Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- Gao, Y., et al. (2023). "Retrieval-Augmented Generation for Large Language Models: A Survey"

### Embedding & Retrieval
- Reimers, N., & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
- Khattab, O., & Zaharia, M. (2020). "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT"

### Chunking Strategies
- Shi, W., et al. (2023). "Replug: Retrieval-augmented black-box language models"

## Open Source Community

Special thanks to the open source communities that make projects like this possible:
- Python Software Foundation
- NumPy, Pandas, and SciPy communities
- The broader AI/ML research community

## Contributors

- Project maintainers and contributors
- Community members who provide feedback and bug reports

---

## How to Cite

If you use this project in your research, please cite:

```bibtex
@software{rag_chatbot_mcp,
  title = {RAG Chatbot MCP Platform},
  year = {2025},
  url = {https://github.com/your-org/rag-chatbot-mcp}
}
```

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
