FROM python:3.8

EXPOSE 5000

ADD requirements.txt requirements.txt
ADD src src
ADD resources resources

RUN pip install -r requirements.txt
ENTRYPOINT python src/youtube-downloader.py