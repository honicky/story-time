from pytorch/pytorch:latest

WORKDIR /

RUN pip install runpod

ADD handler.py .

CMD [ "python", "-u", "/handler.py" ]