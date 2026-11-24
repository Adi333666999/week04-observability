FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -r -u 10001 appuser
COPY --chown=10001:10001 . .
EXPOSE 5000
USER 10001
CMD ["python", "app.py"]