FROM python:3.8-alpine
COPY . /app
WORKDIR  /app
RUN pip install -r requirements_raspi.txt
CMD node app.py

