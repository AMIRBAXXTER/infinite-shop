FROM python:3.11

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

ENV POSTGRES_DB=infinite-shop
ENV POSTGRES_USER=shop_admin
ENV POSTGRES_PASSWORD=12345678
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
