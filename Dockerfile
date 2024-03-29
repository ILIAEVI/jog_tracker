FROM python:3.11.4

RUN mkdir -p /opt/services/djangoapp/src

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000



