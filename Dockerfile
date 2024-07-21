FROM python:3.10

EXPOSE 5000/tcp

WORKDIR /

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD [ "python", "./app.py" ]

#CMD tail -f /dev/null
