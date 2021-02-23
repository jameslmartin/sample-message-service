FROM python:3.7

RUN apt-get update && apt-get install -y postgresql
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY wsgi.py /home/app/
COPY config.py /home/app/
COPY message_service/ /home/app/message_service/
WORKDIR /home/app/

# Use Gunicorn to run Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
