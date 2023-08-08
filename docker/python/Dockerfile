FROM python:3.8-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update && apk add --no-cache --virtual bash gcc musl-dev linux-headers jpeg-dev zlib-dev mariadb-dev libffi-dev

# install pypi packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN rm /usr/bin/mysql*
COPY uwsgi.ini /uwsgi.ini
RUN pip freeze > newreqs.txt

CMD ["uwsgi", "--ini", "/uwsgi.ini"]
