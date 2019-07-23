FROM python:3.6.9-alpine

RUN apk add --no-cache bash

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN  python3 -m venv venv
CMD  ["source venv/bin/activate"]

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /

RUN chmod +x startup.sh

ENTRYPOINT ["/bin/bash", "startup.sh"]

EXPOSE 8080
