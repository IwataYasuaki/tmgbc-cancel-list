FROM python:latest
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    sudo \
    wget \
    vim
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry self add poetry-plugin-export
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt && \
    pip install -r /requirements.txt
CMD ["/bin/bash"] 
