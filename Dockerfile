# FROM python:3.11-slim-buster
FROM python:3.10.14-slim-bullseye
RUN apt update -y
WORKDIR /app

COPY . /app
ENV MY_ENV=MONGODB_URL_KEY
RUN pip3 install -r requirements.txt
# RUN pip install numpy==1.24.4
# RUN chmod +x main.py

CMD ["python3", "main.py"]