FROM python:3.10.5-bullseye

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY URLShortener/ .

CMD [ "python", "manage.py", "runserver" ]
