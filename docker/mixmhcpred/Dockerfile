FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    mafft \
    tar \
    && rm -rf /var/lib/apt/lists/*

COPY MixMHCpred.tar.gz /opt/

WORKDIR /opt

RUN tar -xzf MixMHCpred.tar.gz \
    && mix_dir="$(find /opt -maxdepth 2 -type f -name MixMHCpred -printf '%h\n' | head -n 1)" \
    && test -n "$mix_dir" \
    && pip install --no-cache-dir -r "$mix_dir/code/setup_pythonLibrary.txt" \
    && chmod +x "$mix_dir/MixMHCpred" \
    && printf '#!/bin/sh\nexec "%s/MixMHCpred" "$@"\n' "$mix_dir" > /usr/local/bin/MixMHCpred \
    && chmod +x /usr/local/bin/MixMHCpred

CMD ["MixMHCpred", "-h"]
