FROM python:3.10-slim-buster

WORKDIR /app

COPY ./app ./
COPY ./llms ./llms
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /app/requirements.txt 
#--no-cache-dir
COPY ./entrypoint.sh ./

ENTRYPOINT ["sh","/app/entrypoint.sh"]