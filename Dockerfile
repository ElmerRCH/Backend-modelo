
FROM python:3.9.18-slim-bullseye AS base
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libgl1-mesa-dri \
        libglib2.0-0 \
        gcc\
        python3-dev\
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt
# stage production
FROM base AS production
COPY . /app
RUN mkdir -p /app/static
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]