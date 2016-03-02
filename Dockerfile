FROM python:2.7
MAINTAINER judy.programer@gmail.com
EXPOSE 5000

RUN mkdir /usr/app
WORKDIR /usr/app
ADD requirements.txt ./
RUN pip install -r requirements.txt --index-url http://pypi.douban.com/simple
ADD . .

CMD gunicorn -b 0.0.0.0:5000 --access-logfile "-" app:app
