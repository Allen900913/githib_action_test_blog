# =========================
# Stage 1: Build environment
# =========================
FROM python:3.12-alpine AS builder

WORKDIR /opt/myblog

# 安裝 build 階段需要的套件
RUN apk add --no-cache \
    build-base \
    pkgconfig \
    mariadb-dev

# 建立虛擬環境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 複製需求檔案並安裝套件
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# =========================
# Stage 2: Runtime environment
# =========================
FROM python:3.12-alpine AS runtime

WORKDIR /opt/myblog

# 安裝 runtime 需要的最小依賴
RUN apk add --no-cache mariadb-connector-c

# 從 builder 複製虛擬環境和程式碼
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/myblog /opt/myblog

# 設定 PATH 與 PYTHONPATH
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/opt/myblog

# 啟動程式
ENTRYPOINT ["python", "main.py"]


# =========================
# Stage 1: Build environment
# =========================
# FROM ubuntu:22.04 AS builder

# WORKDIR /opt/myblog

# # 安裝系統依賴 (編譯需要)
# RUN apt-get update \
#     && apt-get install -y python3 python3-pip python3-venv pkg-config libmysqlclient-dev \
#     && rm -rf /var/lib/apt/lists/*

# # 建立虛擬環境
# RUN python3 -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # 複製需求檔案並安裝套件
# COPY requirements.txt .
# RUN pip install --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # 複製專案程式碼
# COPY . .

# # =========================
# # Stage 2: Runtime environment
# # =========================
# FROM ubuntu:22.04 AS runtime

# WORKDIR /opt/myblog

# # 安裝最少系統依賴 (只需 runtime lib，不用 dev headers)
# RUN apt-get update \
#     && apt-get install -y python3 libmysqlclient21 \
#     && rm -rf /var/lib/apt/lists/*

# # 從 builder 複製虛擬環境和程式碼
# COPY --from=builder /opt/venv /opt/venv
# COPY --from=builder /opt/myblog /opt/myblog

# # 設定 PATH 與 PYTHONPATH
# ENV PATH="/opt/venv/bin:$PATH"
# ENV PYTHONPATH=/opt/myblog

# # 啟動程式
# ENTRYPOINT ["python", "main.py"]



# FROM ubuntu

# COPY . /opt/myblog/

# WORKDIR /opt/myblog/

# # 安裝系統依賴
# RUN apt-get update \
#     && apt-get install -y python3 python3-pip python3-venv pkg-config libmysqlclient-dev \
#     && rm -rf /var/lib/apt/lists/*

# # 建立虛擬環境
# RUN python3 -m venv /opt/venv

# # 確保虛擬環境優先於系統 Python
# ENV PATH="/opt/venv/bin:$PATH"

# # 安裝 Python 套件
# RUN pip install --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # 設定 PYTHONPATH
# ENV PYTHONPATH=/opt/myblog

# # 啟動程式
# ENTRYPOINT ["python", "main.py"]
