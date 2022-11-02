FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt apt-get update \
    && apt-get install -y gettext libqpdf-dev xvfb fonts-noto-color-emoji fonts-unifont libfontconfig1 libfreetype6  \
      xfonts-cyrillic xfonts-scalable fonts-liberation fonts-ipafont-gothic fonts-wqy-zenhei fonts-tlwg-loma-otf  \
      fonts-freefont-ttf libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libdbus-1-3  \
      libdrm2 libgbm1 libglib2.0-0 libnspr4 libnss3 libpango-1.0-0 libwayland-client0 libx11-6 libxcb1 libxcomposite1  \
      libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 libcairo-gobject2 libdbus-glib-1-2 libegl1  \
      libenchant-2-2 libepoxy0 libevdev2 libgdk-pixbuf-2.0-0 libgles2 libglx0 libgstreamer-plugins-base1.0-0  \
      libgstreamer1.0-0 libgstreamer-gl1.0-0 libgtk-3-0 libgudev-1.0-0 libharfbuzz-icu0 libharfbuzz0b libhyphen0  \
      libicu67 libjpeg62-turbo liblcms2-2 libmanette-0.2-0 libnotify4 libopengl0 libopenjp2-7 libopus0  \
      libpangocairo-1.0-0 libpng16-16 libproxy1v5 libsecret-1-0 libsoup2.4-1 libwayland-egl1 libwayland-server0  \
      libwebp6 libwebpdemux2 libwoff1 libx11-xcb1 libxcb-shm0 libxcursor1 libxi6 libxml2 libxrender1 libxslt1.1  \
      libxtst6 libatomic1 libevent-2.1-7

RUN --mount=type=cache,target=/root/.cache pip install --upgrade pip && pip install -r requirements.txt
RUN playwright install chromium
