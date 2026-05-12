FROM --platform=linux/amd64 ubuntu:22.04

RUN apt-get update && apt-get install -y \
    perl gawk tcsh wget tar sed libc6

WORKDIR /opt

COPY netChop.tar.gz /opt/
RUN tar -xzf netChop.tar.gz

RUN ln -s /opt/netchop-3.1/Linux_x86_64/bin /opt/netchop-3.1/bin

RUN mkdir -p /etc && \
    ln -s /opt/netchop-3.1/etc/Cterm.3.0 /etc/Cterm.3.0

ENV NMHOME=/opt/netchop-3.1
ENV NETCHOP=/opt/netchop-3.1
ENV TMPDIR=/tmp
ENV PATH="/opt/netchop-3.1/bin:$PATH"

CMD ["bash"]
