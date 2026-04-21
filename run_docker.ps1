# run_docker.ps1 — Build and run the mlops-task container on Windows
# Usage: .\run_docker.ps1

$PROJECT = "C:\Users\Ahmed Pasha\Desktop\task"
$IMAGE   = "mlops-task"

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker build --no-cache -t $IMAGE $PROJECT

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

Write-Host "Running container..." -ForegroundColor Cyan
docker run --rm `
  -v "${PROJECT}:/data" `
  $IMAGE `
  python run.py `
    --input   /data/data.csv `
    --config  /data/config.yaml `
    --output  /data/metrics.json `
    --log-file /data/run.log

Write-Host "Done. Check metrics.json and run.log in your project folder." -ForegroundColor Green
