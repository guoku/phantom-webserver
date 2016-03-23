FROM python:2.7
MAINTAINER judy.programer@gmail.com
EXPOSE 5000

ENV PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple
RUN mkdir /usr/app
WORKDIR /usr/app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD . .

CMD gunicorn -b 0.0.0.0:5000 -t 180 --access-logfile "-" app:app
