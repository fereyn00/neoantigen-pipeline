FROM python:3.10-slim

ARG MHCFLURRY_VERSION=2.2.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "mhcflurry==${MHCFLURRY_VERSION}" \
    && mhcflurry-downloads fetch models_class1_presentation

CMD ["mhcflurry-predict", "--help"]
