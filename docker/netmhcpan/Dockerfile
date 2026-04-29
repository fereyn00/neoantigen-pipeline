FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    tcsh gawk perl wget make gcc tar sed

COPY netMHCpan.tar.gz /opt/

WORKDIR /opt

RUN tar -xzf netMHCpan.tar.gz

# Fix hardcoded install path inside wrapper script
RUN sed -i 's|/tools/src/netMHCpan-4.2|/opt/netMHCpan-4.2|' \
    /opt/netMHCpan-4.2/netMHCpan

# Optional but recommended: ensure correct permissions
RUN chmod +x /opt/netMHCpan-4.2/netMHCpan \
             /opt/netMHCpan-4.2/Linux_aarch64/bin/*

ENV NMHOME=/opt/netMHCpan-4.2
ENV PATH="$NMHOME:$PATH"

CMD ["tcsh"]
