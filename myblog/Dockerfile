FROM python:3.12-alpine AS builder

WORKDIR /opt/myblog

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-alpine AS runtime

WORKDIR /opt/myblog

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/myblog /opt/myblog

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/opt/myblog

ENTRYPOINT ["python", "main.py"]
