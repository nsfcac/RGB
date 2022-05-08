from centos:centos7

RUN yum -y install python3 \
	&& python3 -m pip install --user --upgrade pip
WORKDIR /app

COPY . /app

RUN python3 -m pip --no-cache-dir install --user -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["app.py"]
