FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y cron
COPY tests/ml-work-cronjob /etc/cron.d/ml-work-cronjob

RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /code/
COPY src/mnist/run.sh /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/NishNovae/mnist.git@0.4.0

CMD ["sh", "run.sh"]
