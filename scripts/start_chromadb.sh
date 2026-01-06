#!/bin/bash
# Start ChromaDB in Docker

echo "Starting ChromaDB in Docker..."
docker-compose up -d chromadb

echo "Waiting for ChromaDB to be ready..."
sleep 5

# Check if ChromaDB is running
if curl -f http://localhost:8000/api/v1/heartbeat > /dev/null 2>&1; then
    echo "✅ ChromaDB is running at http://localhost:8000"
else
    echo "⚠️ ChromaDB may still be starting. Check with: docker-compose logs chromadb"
fi

echo ""
echo "To stop ChromaDB: docker-compose down"
echo "To view logs: docker-compose logs -f chromadb"

