# Stage 1: Build the Rust Scanner
FROM rust:latest as builder
WORKDIR /usr/src/rgb-tools
COPY rgb-tools/ .
RUN cargo build --release --bin rgb-scanner

# Stage 2: Python Runtime & Explorer
FROM python:3.11-slim
WORKDIR /app/explorer

# Copy the scanner binary
COPY --from=builder /usr/src/rgb-tools/target/release/rgb-scanner /usr/local/bin/rgb-scanner

# Copy the explorer frontend/backend code
# We copy everything so the container is standalone
COPY explorer/ .

# Environment setup
ENV RGB_SCANNER_PATH=/usr/local/bin/rgb-scanner
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "server.py"]
