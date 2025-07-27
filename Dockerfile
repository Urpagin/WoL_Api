FROM python:3.13-slim

WORKDIR /app_data

COPY ./backend/ /app_data/backend/
COPY ./frontend/ /app_data/frontend/

RUN pip install -r backend/requirements.txt

EXPOSE 53562

CMD python ./backend/main.py
