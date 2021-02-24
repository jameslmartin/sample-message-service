FROM python:3.7

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY wsgi.py /home/app/
COPY config.py /home/app/
COPY app/ /home/app/app/
WORKDIR /home/app/

# Use Gunicorn to run Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
