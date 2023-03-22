FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app



# Define environment variable for database connection
ENV POSTGRES_USER=parser_user
ENV POSTGRES_PASSWORD=parser
ENV POSTGRES_DB=population_db

CMD ["python", "main.py"]
