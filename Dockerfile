FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MODEL_PATH=conanWinner/model_scheduler \
    PORT=5000 \
    HOST=0.0.0.0 \
    DEBUG=False \
    USE_FP16=False

WORKDIR /app

# Copy requirements riêng để tối ưu cache layer
COPY requirements.txt .

# Cài đặt dependencies và cleanup
# Sử dụng torch CPU-only để giảm dung lượng (~500MB thay vì ~2GB+ với CUDA)
# Cài torch trước, sau đó cài các packages khác (tránh xung đột version)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip /root/.cache/huggingface /tmp/pip-*

# Copy app code
COPY . .

EXPOSE 5000

CMD ["python", "main.py"]