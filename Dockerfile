FROM rosenhouse/phantomjs2
MAINTAINER judy.programer@gmail.com
EXPOSE 5000

COPY aliyun.sources.list /etc/apt/sources.list
RUN apt-get update -yqq && apt-get install -y python-pip

RUN mkdir /usr/app
WORKDIR /usr/app
ADD requirements.txt ./
RUN pip install -r requirements.txt --index-url http://pypi.douban.com/simple
ADD . .

CMD gunicorn -b 0.0.0.0:5000 --access-logfile "-" app:app
