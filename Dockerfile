FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./.env.docker /code/src/.env
COPY ./.env.docker /code/.env
COPY ./setup.cfg /code/setup.cfg
COPY ./pytest.ini /code/pytest.ini
COPY ./dockerization/start.sh /code/start.sh

COPY ./src /code/src