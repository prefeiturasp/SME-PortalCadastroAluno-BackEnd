FROM python:3.6-alpine3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
COPY . /code/

WORKDIR /code

RUN apk update && apk add postgresql-dev tzdata && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
      apk add --no-cache \
      --virtual=.build-dependencies \
      gcc \
      g++ \
      musl-dev \
      git \
      python3-dev \
      jpeg-dev \
      # Pillow
      zlib-dev \
      freetype-dev \
      lcms2-dev \
      openjpeg-dev \
      tiff-dev \
      tk-dev \
      tcl-dev \
      harfbuzz-dev \
      fribidi-dev \
      make
RUN python -m pip --no-cache install -U pip
RUN pip install -r requirements/local.txt

EXPOSE 8000
CMD ["make", "start_docker"]

