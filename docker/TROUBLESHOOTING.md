# ChromaDB Docker Troubleshooting

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Python 3.14 Compatibility Issue

**Problem:** ChromaDB has compatibility issues with Python 3.14+ due to pydantic v1 dependencies.

**Symptoms:**
- `pydantic.v1.errors.ConfigError: unable to infer type for attribute "chroma_server_nofile"`
- ChromaDB falls back to mock mode

**Solutions:**

### Option 1: Use Python 3.11 or 3.12 (Recommended)
```bash
# Install Python 3.12
# Then create a virtual environment
python3.12 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
pip install chromadb
```

### Option 2: Use Mock Mode (Current Workaround)
The application will automatically use mock mode if ChromaDB cannot be imported. This works but has limited functionality:
- ✅ Document storage and retrieval works
- ✅ Vector search works (simplified)
- ⚠️ Data is not persisted between sessions
- ⚠️ Some advanced features may not work

### Option 3: Use ChromaDB HTTP API Directly
You can connect to ChromaDB Docker via HTTP requests without the Python client:
```python
import requests

# Example: List collections
response = requests.get("http://localhost:8000/api/v1/collections")
print(response.json())
```

## Docker Issues

### ChromaDB Container Won't Start
```bash
# Check logs
docker-compose logs chromadb

# Restart container
docker-compose restart chromadb

# Remove and recreate
docker-compose down
docker-compose up -d chromadb
```

### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead of 8000

# Update environment variables
export CHROMA_PORT=8001
```

### Connection Refused
```bash
# Verify ChromaDB is running
docker-compose ps

# Check if port is accessible
curl http://localhost:8000/api/v1/heartbeat

# Wait a few seconds after starting - ChromaDB needs time to initialize
```

## Current Status

With Python 3.14:
- ✅ ChromaDB Docker container runs fine
- ⚠️ Python client has import issues
- ✅ Application falls back to mock mode gracefully
- ✅ Mock mode works for testing and learning

**Recommendation:** For production use, use Python 3.11 or 3.12. For development/testing, mock mode works fine.

