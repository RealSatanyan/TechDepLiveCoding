FROM python:3.13-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]