FROM ubuntu:latest
FROM pytorch/pytorch:latest

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
# Dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        tini \
        python3-pip \
        python3-dev \
        python3-opencv \
        libglib2.0-0


WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH /usr/app

COPY . .

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
