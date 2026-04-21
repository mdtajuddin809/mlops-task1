FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]