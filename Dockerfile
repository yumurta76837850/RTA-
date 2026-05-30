FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nasm \
    binutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
COPY . .

RUN python -c "import sys; sys.path.insert(0, '/app'); from src.compiler import main" || true

ENTRYPOINT ["python", "compiler.py"]
CMD ["--help"]
