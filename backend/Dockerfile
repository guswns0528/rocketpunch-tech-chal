FROM python:3.8

RUN pip install -r requirements.txt
WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
