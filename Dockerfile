FROM python

RUN apt-get update -y && \  
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN  apt-get install -y python3-venv && python3 -m venv venv
CMD  ["source venv/bin/activate"]

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /

RUN chmod +x startup.sh

ENTRYPOINT ["/bin/bash", "startup.sh"]

EXPOSE 8080
