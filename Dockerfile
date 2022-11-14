FROM python:3.10-slim
WORKDIR /app
ENV TZ=Asia/Shanghai
COPY --chmod=755 . /app/
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "/app/telecha.docker.py"]
