# Stage 1 — builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies first 
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .


# Stage 2 — runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create non-root user
RUN useradd -m -u 10001 appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY --from=builder /app/app ./app

# Drop privileges
USER appuser

EXPOSE 8000

# Start FastAPI via uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]