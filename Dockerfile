FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY --chown=10000:10001 . /app/
USER 10000:10001
CMD python app/main.py
