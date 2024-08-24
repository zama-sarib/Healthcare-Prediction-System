FROM python:3.8.5-slim-buster
RUN apt update -y
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN pip install numpy==1.24.4
RUN chmod +x main.py

CMD ["python3", "main.py"]