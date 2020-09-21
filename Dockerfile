FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
    && apt-get -y install git locales libpq-dev postgresql-client vim graphviz libgraphviz-dev \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Set timezone
ENV TZ=Pacific/Auckland
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN echo 'en_NZ.UTF-8 UTF-8' > /etc/locale.gen && locale-gen en_NZ.UTF-8
ENV LANG en_NZ.UTF-8

# Copy all requirements files so Docker is aware of any future changes
COPY requirements.txt requirements.txt

# Create virtualenv and install requirements
ENV PATH /virtualenv/bin:$PATH
ENV VIRTUAL_ENV /virtualenv
RUN python3 -m venv /virtualenv
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

WORKDIR /code
