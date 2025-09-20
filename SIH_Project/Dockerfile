# 1. Start from a lightweight official Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy all project files into /app
COPY . .

# 5. Expose port 5000
EXPOSE 5000

# 6. Start the Flask app
CMD ["python", "app.py"]
