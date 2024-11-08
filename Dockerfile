FROM python:3.12

WORKDIR /code

COPY ./host/requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade -r requirements.txt

COPY ./host .
COPY ./version.txt .

CMD ["python", "/code/main.py"]