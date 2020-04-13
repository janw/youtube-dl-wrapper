FROM registry.gitlab.com/janw/python-poetry:3.8-alpine as requirements

COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt -o requirements.txt


FROM lsiobase/alpine:3.11
ARG BUILD_DATE
ARG VCS_REF

COPY --from=requirements /src/requirements.txt /
RUN apk add --no-cache ca-certificates wget ffmpeg python3 gnupg bash su-exec && \
    pip3 install -r /requirements.txt

COPY root/ /
COPY entrypoint.sh /
COPY config/ /config
COPY youtube_dl_wrapper /src/youtube_dl_wrapper

VOLUME /downloads
VOLUME /config
