FROM python:3.7.2-alpine3.9

COPY crontab /etc/cron/crontab
RUN crontab /etc/cron/crontab

RUN apk --no-cache add ca-certificates \
		firefox-esr \
		wget

RUN cd /tmp \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
    && tar xvfz geckodriver-v0.23.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin \
    && rm geckodriver-v0.23.0-linux64.tar.gz

ADD requirements.txt /usr/local
RUN pip3 install -r /usr/local/requirements.txt

ADD oneclick.py /usr/local
WORKDIR /usr/local

ENV ONECLICKURL="https://one-click.de/html" \
    CLIENTNUMBER=1 \
    USERNAME="user" \
    PASSWORD="pass" \
    TELEGRAMBOTKEY="bot4711" \
    CHATID=4711

#CMD ["python3", "oneclick.py"]
CMD ["crond", "-f"]