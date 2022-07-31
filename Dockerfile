# Uses python slim version
FROM python:slim

# Default python image directory
WORKDIR /usr/src/app

# Install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole app
COPY ./src .
ENTRYPOINT [ "python", "./ouigo-searcher/ouigo.py" ]