# syntax=docker/dockerfile:1

FROM python:3.13-alpine@sha256:2d9aefe2fef018a7eb2c13064c89c71929800fd2e5dccdbf52ea5da5bb8d929a

ARG ISSUE_DIR=example_issue

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8023 \
    CONTENT_FOLDER=issue

WORKDIR /app

COPY requirements-runtime.txt requirements-runtime.txt
RUN apk add --no-cache zlib=1.3.2-r1 \
    && python -m pip install --no-cache-dir --require-hashes --only-binary=:all: -r requirements-runtime.txt \
    && python -m pip uninstall --yes pip \
    && addgroup -g 10001 app \
    && adduser -D -H -u 10001 -G app -s /sbin/nologin app

# Keep runtime files root-owned and leave the HTML generator out of the image.
COPY dialazine/lib/common_tools.py \
     dialazine/lib/contents_reader.py \
     dialazine/lib/text_screen_reader.py \
     dialazine/lib/zine_functions.py ./dialazine/lib/
COPY dialazine/server.py ./dialazine/server.py
COPY ${ISSUE_DIR}/ ./issue/
COPY LICENSE ./LICENSE

USER 10001:10001
EXPOSE 8023/tcp

CMD ["python", "dialazine/server.py"]
