"""
MCP Generator Server

Response generation for RAG pipelines.
"""

import json
import logging
from typing import Any, Optional, List, Dict

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    Server = None
    stdio_server = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeneratorManager:
    """Manages response generation."""
    
    DEFAULT_TEMPLATES = {
        "default": """Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:""",
        
        "concise": """Answer briefly based on the context.

Context: {context}

Question: {query}

Brief answer:""",
        
        "detailed": """Provide a comprehensive answer using the given context.

Context:
{context}

Question: {query}

Detailed answer with explanations:""",
        
        "citation": """Answer the question and cite your sources.

Context:
{context}

Question: {query}

Answer (include [1], [2], etc. for citations):"""
    }
    
    def __init__(self):
        self.templates = self.DEFAULT_TEMPLATES.copy()
        
    def _format_context(self, documents: List[Dict]) -> str:
        """Format documents into context string."""
        formatted = []
        for i, doc in enumerate(documents, 1):
            text = doc.get("text", doc.get("content", ""))
            source = doc.get("metadata", {}).get("source", f"Document {i}")
            formatted.append(f"[{i}] {source}:\n{text}")
        return "\n\n".join(formatted)
    
    def _mock_generate(self, prompt: str) -> str:
        """Mock generation for development."""
        # Extract key terms from context
        lines = prompt.split("\n")
        context_lines = [l for l in lines if l.strip() and not l.startswith("Question")]
        
        if "Question:" in prompt:
            question = prompt.split("Question:")[-1].split("\n")[0].strip()
        else:
            question = "the query"
        
        return f"Based on the provided context, here is the answer to {question}: The documents indicate relevant information that addresses your question. Please note that this is a mock response for development purposes."
    
    def generate_response(self, query: str, context: List[Dict],
                         template: str = "default") -> dict:
        """Generate answer from context."""
        template_str = self.templates.get(template, self.templates["default"])
        context_str = self._format_context(context)
        
        prompt = template_str.format(context=context_str, query=query)
        response = self._mock_generate(prompt)
        
        return {
            "status": "success",
            "query": query,
            "response": response,
            "template": template,
            "context_docs": len(context),
            "prompt_length": len(prompt)
        }
    
    def summarize_context(self, documents: List[Dict], 
                         max_length: int = 500) -> dict:
        """Summarize retrieved documents."""
        context_str = self._format_context(documents)
        
        # Mock summarization
        words = context_str.split()
        if len(words) > max_length // 5:
            summary = " ".join(words[:max_length // 5]) + "..."
        else:
            summary = context_str
        
        return {
            "status": "success",
            "summary": f"Summary of {len(documents)} documents: {summary[:max_length]}",
            "original_length": len(context_str),
            "summary_length": min(len(summary), max_length),
            "documents_summarized": len(documents)
        }
    
    def extract_info(self, documents: List[Dict], schema: Dict) -> dict:
        """Extract structured information from documents."""
        context_str = self._format_context(documents)
        
        # Mock extraction based on schema
        extracted = {}
        for field, field_schema in schema.get("properties", {}).items():
            field_type = field_schema.get("type", "string")
            
            # Mock extraction
            if field_type == "string":
                extracted[field] = f"Extracted {field} from documents"
            elif field_type == "number":
                extracted[field] = 0
            elif field_type == "array":
                extracted[field] = []
            elif field_type == "boolean":
                extracted[field] = False
        
        return {
            "status": "success",
            "extracted": extracted,
            "schema": schema,
            "source_documents": len(documents)
        }
    
    def generate_with_citations(self, query: str, context: List[Dict]) -> dict:
        """Generate response with source citations."""
        context_str = self._format_context(context)
        
        prompt = self.templates["citation"].format(context=context_str, query=query)
        
        # Generate response with mock citations
        response_parts = []
        response_parts.append(f"Based on the available sources, here is the answer to your question about '{query}':")
        
        for i, doc in enumerate(context[:3], 1):
            text = doc.get("text", "")[:100]
            response_parts.append(f"\nAccording to source [{i}]: {text}...")
        
        response = " ".join(response_parts)
        
        citations = [
            {
                "index": i,
                "source": doc.get("metadata", {}).get("source", f"Document {i}"),
                "text_snippet": doc.get("text", "")[:200]
            }
            for i, doc in enumerate(context, 1)
        ]
        
        return {
            "status": "success",
            "query": query,
            "response": response,
            "citations": citations,
            "num_citations": len(citations)
        }
    
    def set_prompt_template(self, name: str, template: str) -> dict:
        """Configure custom prompt template."""
        self.templates[name] = template
        
        return {
            "status": "success",
            "template_name": name,
            "message": f"Template '{name}' configured successfully",
            "available_templates": list(self.templates.keys())
        }


# Initialize
app = Server("mcp-generator") if Server else None
manager = GeneratorManager()

TOOLS = [
    Tool(
        name="generate_response",
        description="Generate answer from retrieved context",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "context": {"type": "array", "items": {"type": "object"}},
                "template": {"type": "string", "enum": ["default", "concise", "detailed", "citation"]}
            },
            "required": ["query", "context"]
        }
    ),
    Tool(
        name="summarize_context",
        description="Summarize retrieved documents",
        inputSchema={
            "type": "object",
            "properties": {
                "documents": {"type": "array", "items": {"type": "object"}},
                "max_length": {"type": "integer", "default": 500}
            },
            "required": ["documents"]
        }
    ),
    Tool(
        name="extract_info",
        description="Extract structured information from documents",
        inputSchema={
            "type": "object",
            "properties": {
                "documents": {"type": "array", "items": {"type": "object"}},
                "schema": {"type": "object"}
            },
            "required": ["documents", "schema"]
        }
    ),
    Tool(
        name="generate_with_citations",
        description="Generate response with source citations",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "context": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["query", "context"]
        }
    ),
    Tool(
        name="set_prompt_template",
        description="Configure custom prompt template",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "template": {"type": "string"}
            },
            "required": ["name", "template"]
        }
    )
]

if app:
    @app.list_tools()
    async def list_tools():
        return TOOLS

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "generate_response":
                result = manager.generate_response(**arguments)
            elif name == "summarize_context":
                result = manager.summarize_context(**arguments)
            elif name == "extract_info":
                result = manager.extract_info(**arguments)
            elif name == "generate_with_citations":
                result = manager.generate_with_citations(**arguments)
            elif name == "set_prompt_template":
                result = manager.set_prompt_template(**arguments)
            else:
                result = {"error": f"Unknown tool: {name}"}
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            logger.error(f"Error in {name}: {e}")
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    if stdio_server:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
