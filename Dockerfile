FROM python:3.11.3-slim-buster
WORKDIR /app_data
COPY ./main.py /app_data
COPY ./wol.py /app_data
COPY ./add_machine.py /app_data
COPY ./index.html /app_data
COPY ./static/favicon.svg /app_data/static/
COPY ./.env /app_data
COPY ./requirements.txt /app_data
RUN pip install -r requirements.txt
EXPOSE 53562
CMD python ./main.py