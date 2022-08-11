FROM ubuntu:22.04

COPY . /app
WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python3-pip -y && \
    pip3 install -r requirements.txt
    
EXPOSE 5000

CMD ["python3","recommend_api.py"]