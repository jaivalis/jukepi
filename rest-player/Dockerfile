FROM python:3-alpine

ADD player /player

RUN pip install -r player/requirements.txt

WORKDIR player

EXPOSE 8888

CMD [ "python", "-m", "app" ]
