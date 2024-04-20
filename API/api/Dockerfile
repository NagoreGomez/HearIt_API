FROM python:3.10

WORKDIR /hearit_api

RUN pip install --upgrade pip

COPY requirements.txt /hearit_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /hearit_api/requirements.txt

COPY ./app /hearit_api/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

