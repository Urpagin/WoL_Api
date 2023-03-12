FROM python:3-alpine3.17
WORKDIR /app_data
COPY ./app.py /app_data
COPY ./wol.py /app_data
COPY ./requirements.txt /app_data
RUN pip install -r requirements.txt
EXPOSE 38051
CMD python ./app.py