# Use a more specific Python image
FROM python:3.9-slim AS builder

WORKDIR /app

# Create a virtual environment and set it as the active environment
RUN python -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy only the requirements file and install FastAPI and Uvicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

# Use a separate stage for the runner
FROM python:3.9-slim AS runner

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv venv

# Copy the FastAPI application code
COPY main.py main.py

# Set the virtual environment path
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose the port (optional)
EXPOSE 8000

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
