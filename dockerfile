# syntax=docker/dockerfile:1
FROM python:3-alpine3.15

WORKDIR /src

# get source code
COPY src/* /src
COPY requirements.txt /src

# install app dependencies
RUN pip install -r requirements.txt

# final configuration
EXPOSE 3000
CMD ["python3", "."]