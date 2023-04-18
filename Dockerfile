FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN curl 'https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh' -o /wait-for-it.sh && \
    chmod 755 /wait-for-it.sh

RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y gettext libqpdf-dev \
    # chromium dependencies for debian
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libatspi2.0-0 libxcomposite1  \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libdrm2 libxkbcommon0 libasound2 libwayland-client0

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache pip install --upgrade pip && pip install -r requirements.txt

RUN playwright install chromium

RUN git config --system --replace-all safe.directory '*'
