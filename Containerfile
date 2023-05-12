FROM python:3.10-alpine

WORKDIR /app

COPY . .
COPY requirements.txt .

RUN apk update \
 && apk upgrade \
 && apk add --no-cache bash git openssh vim libffi-dev gcc libc-dev linux-headers postgresql-dev

RUN python3.10 -m pip install pip --upgrade

RUN pip install -r ./requirements.txt

# --proxi-headers is added when the container behind a TLS terminal proxy like nginx or traefik
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--reload"]
