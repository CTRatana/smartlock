# Builder Stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Create a virtual environment
RUN python -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Runner Stage
FROM python:3.9-slim AS runner

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv venv

COPY . .

COPY main.py main.py

# Set environment variables to activate the virtual environment
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose port 8000
EXPOSE 8000

# Specify the entry point to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
