FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY uv.lock .

RUN pip install uv && uv pip install --system -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
