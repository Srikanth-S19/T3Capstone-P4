# 1. Use an official, lightweight Python base image
FROM python:3.10-slim

# 2. Set environment variables to optimize Python execution in Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies if required (slim images contain minimal libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# 6. Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 7. Copy the application source code and the trained serialized model artifact
# Ensure 'main.py' and 'churn_model.pkl' are present in your local directory
COPY main.py /app/
COPY model.pkl /app/
COPY metrics.json /app/

# 8. Expose the internal port that Uvicorn binds to
EXPOSE 8000

# 9. Run the application using Uvicorn server when the container boots
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
