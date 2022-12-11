FROM python

ADD net.py /

RUN apt-get update
RUN apt install -y iputils-ping


CMD ["python3", "./net.py"]