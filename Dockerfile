# syntax=docker/dockerfile:1
FROM debian:bullseye-slim AS locales
WORKDIR locales/
COPY ./locales ./
RUN apt-get update -qq
RUN apt-get install -qq -y gettext
RUN find ./ -name \*.po -execdir msgfmt bot.po -o bot.mo \;

FROM python:3.10-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH=${PATH}:${PYTHONPATH}/bin
WORKDIR ${PYTHONPATH}
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
RUN mkdir -p /root/.cache/
RUN getmodels
COPY --from=locales locales/ locales/
COPY --from=jrottenberg/ffmpeg:scratch / /
CMD ["python", "src/main.py"]
