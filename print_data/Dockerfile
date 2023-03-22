FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY print_data.py /app


CMD ["python", "print_data.py"]
