# syntax=docker/dockerfile:1
FROM python:3-alpine3.13

WORKDIR /app

# get source code
COPY ./src /app/
COPY requirements.txt /app/

# install app dependencies
RUN pip install -r requirements.txt

# final configuration
EXPOSE 33507
CMD ["python3", "."]