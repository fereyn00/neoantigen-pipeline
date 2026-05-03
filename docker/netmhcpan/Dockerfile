FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    tcsh gawk perl wget make gcc tar sed

COPY netMHCpan.tar.gz /opt/

WORKDIR /opt

RUN tar -xzf netMHCpan.tar.gz

RUN sed -i 's|/tools/src/netMHCpan-4.2|/opt/netMHCpan-4.2|' \
    /opt/netMHCpan-4.2/netMHCpan

RUN chmod +x /opt/netMHCpan-4.2/netMHCpan \
             /opt/netMHCpan-4.2/Linux_arm64/bin/*

ENV NMHOME=/opt/netMHCpan-4.2
ENV TMPDIR=/tmp
ENV PATH="$NMHOME:$PATH"

CMD ["tcsh"]
