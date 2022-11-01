FROM python:3.11.0-slim AS build-env
COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip install --target=./ --no-cache-dir -r ./requirements.txt

FROM gcr.io/distroless/python3
COPY --from=build-env /app /app

WORKDIR /app
CMD ["cloud.py"]