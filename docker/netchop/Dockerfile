FROM --platform=linux/amd64 ubuntu:22.04

RUN apt-get update && apt-get install -y \
    perl gawk tcsh wget tar sed libc6

WORKDIR /opt

COPY netChop.tar.gz /opt/
RUN tar -xzf netChop.tar.gz

# CRITICAL FIX: flatten expected structure
RUN ln -s /opt/netchop-3.1/Linux_x86_64/bin /opt/netchop-3.1/bin

# FIX model location
RUN mkdir -p /etc && \
    ln -s /opt/netchop-3.1/etc/Cterm.3.0 /etc/Cterm.3.0

# MUST be consistent
ENV NMHOME=/opt/netchop-3.1
ENV NETCHOP=/opt/netchop-3.1
ENV TMPDIR=/tmp
ENV PATH="/opt/netchop-3.1/bin:$PATH"

CMD ["bash"]
