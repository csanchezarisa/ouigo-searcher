FROM python:slim
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "./src/ouigo-searcher/ouigo.py" ]