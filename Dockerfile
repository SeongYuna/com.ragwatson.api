# 프로젝트 venv 기준 Python 3.13
# GPU(CUDA 12.6) 컨테이너 빌드 — 호스트에 NVIDIA Container Toolkit 설치 필요
# 빌드: docker build -t ragwatson-backend ./backend
# 실행(compose 미사용 시): docker run --gpus all ragwatson-backend
FROM nvidia/cuda:12.6.3-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Python 3.13 (deadsnakes PPA) + opencv-python 런타임 의존성 (libGL, glib)
RUN apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common curl libgl1 libglib2.0-0 \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3.13 python3.13-venv python3.13-dev \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
# torch/torchvision은 GPU(cu126) 빌드로 별도 설치한다 (PyPI 기본 인덱스에 cu126 빌드가 없음).
RUN --mount=type=cache,target=/root/.cache/pip \
    python3.13 -m pip install --upgrade pip \
    && grep -v -E "^(torch|torchvision)==" /app/requirements.txt > /app/requirements.docker.txt \
    && python3.13 -m pip install -r /app/requirements.docker.txt \
    && python3.13 -m pip install torch==2.12.1+cu126 torchvision==0.27.1+cu126 --index-url https://download.pytorch.org/whl/cu126

COPY . /app

EXPOSE 8000

CMD ["python3.13", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
