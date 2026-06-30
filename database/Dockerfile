FROM python:3.11-slim
WORKDIR /app
RUN pip install PyMySQL
COPY seed.py .
CMD ["python", "seed.py"]
