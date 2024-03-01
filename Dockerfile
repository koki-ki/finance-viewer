FROM python:3
WORKDIR /app
COPY ./app /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

