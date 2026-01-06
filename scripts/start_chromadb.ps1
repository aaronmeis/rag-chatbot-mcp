# Start ChromaDB in Docker (PowerShell)

Write-Host "Starting ChromaDB in Docker..." -ForegroundColor Green
docker-compose up -d chromadb

Write-Host "Waiting for ChromaDB to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if ChromaDB is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/heartbeat" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ ChromaDB is running at http://localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ ChromaDB may still be starting. Check with: docker-compose logs chromadb" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To stop ChromaDB: docker-compose down" -ForegroundColor Cyan
Write-Host "To view logs: docker-compose logs -f chromadb" -ForegroundColor Cyan

