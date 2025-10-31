FROM python:3.11-slim

# System dependencies for OpenCV (video), audio conversion, and runtime libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY requirements.txt ./

# Install Python dependencies
RUN python -m pip install --upgrade pip \
  && pip install -r requirements.txt

COPY . .

# Streamlit listens on 8501 by default
EXPOSE 8501

# Streamlit needs to bind to 0.0.0.0 in container; PORT env may be provided by platform
ENV PORT=8501 \
    PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "app.py", "--server.port", "${PORT}", "--server.address", "0.0.0.0"]


