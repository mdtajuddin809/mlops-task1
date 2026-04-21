🚀 MLOps Batch Pipeline Project
<p align="center"> <b>Python • Docker • Data Pipeline • MLOps</b><br> <i>End-to-end batch pipeline with reproducible execution</i> </p>
📌 Overview

This project implements a production-style batch processing pipeline that:

Reads financial time-series data from a CSV file
Computes rolling statistics on close prices
Generates binary trading signals
Outputs structured metrics in JSON format

💡 The entire pipeline is Dockerized, ensuring consistent and reproducible execution across environments.

🎯 Objectives
Process structured CSV data
Compute rolling mean on close prices
Generate trading signals (0/1)
Output performance metrics
Enable reproducible runs using Docker
🧠 Tech Stack
Technology	Purpose
🐍 Python 3.11	Core programming
📊 Pandas, NumPy	Data processing
⚙️ YAML	Configuration management
🐳 Docker	Containerization
📂 Project Structure
.
├── run.py              # Main pipeline script
├── config.yaml        # Configuration file
├── data.csv           # Input dataset
├── requirements.txt   # Dependencies
├── Dockerfile         # Container setup
├── metrics.json       # Output metrics
├── run.log            # Execution logs
├── docker_output.png  # Docker execution proof
└── README.md          # Documentation
⚙️ How It Works
🔄 Pipeline Flow
Load configuration from config.yaml
Read CSV dataset
Compute rolling mean
Generate signals:
1 → if close > rolling_mean
0 → otherwise
Compute metrics:
Rows processed
Signal rate
Latency
Save output to metrics.json
▶️ Run Locally
python run.py \
  --input data.csv \
  --config config.yaml \
  --output metrics.json \
  --log-file run.log
🐳 Run with Docker
🔨 Build Image
docker build -t mlops-task .
▶️ Run Container
docker run --rm \
  -v "$(pwd):/data" \
  mlops-task \
  python run.py \
    --input /data/data.csv \
    --config /data/config.yaml \
    --output /data/metrics.json \
    --log-file /data/run.log
📊 Sample Output
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4978,
  "latency_ms": 283,
  "seed": 42,
  "window": 10,
  "status": "success"
}
📝 Logging
Logs stored in run.log
Includes execution flow, configuration, and errors
⚠️ Error Handling
Validates input files
Handles CSV parsing issues
Supports encoding fallback
Ensures JSON output even on failure
🚧 Challenges & Solutions
🔹 CSV Parsing Issues
Faced encoding & delimiter inconsistencies
✔ Solved using flexible parsing (engine="python")
🔹 Docker Compatibility
Differences between Windows & Linux environments
✔ Fixed via standardized file handling
🔹 Dependency Issues
Missing libraries inside Docker
✔ Resolved using requirements.txt
📈 Future Improvements
Add unit testing
CI/CD pipeline integration
Cloud deployment (AWS/GCP)
Real-time streaming support
🐳 Docker Execution Proof

🔗 Project Link

👉 https://github.com/mdtajuddin809/mlops-task1

👤 Author

Mohammed Tajuddin
Aspiring Machine Learning Engineer | MLOps Enthusiast

⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
