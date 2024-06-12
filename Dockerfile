FROM python:3.9

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt

#CMD tail -f /dev/null
