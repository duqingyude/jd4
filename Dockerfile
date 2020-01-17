FROM debian:stretch
COPY . /tmp/jd4
RUN sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list && \
    sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
            gcc \
            python3 \
            python3-venv \
            python3-dev \
            g++ \
            fp-compiler \
            openjdk-8-jdk-headless \
            python \
            php7.2-cli \
            rustc \
            haskell-platform \
            libjavascriptcoregtk-4.0-bin \
            golang \
            ruby \
            mono-runtime \
            mono-mcs && \
    python3 -m venv /venv && \
    bash -c "source /venv/bin/activate && \
             pip install -i https://mirrors.aliyun.com/pypi/simple/ pip==10.0.0 &&\
             pip config set global.index-url http://mirrors.aliyun.com/pypi/simple && \
             pip config set install.trusted-host mirrors.aliyun.com && \
             pip install -r /tmp/jd4/requirements.txt && \
             cd /tmp/jd4/ && \
             python setup.py install" && \
    apt-get remove -y python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /root/.config/jd4 && \
    cp /tmp/jd4/examples/langs.yaml /root/.config/jd4/langs.yaml && \
    cp /tmp/jd4/examples/config.yaml /root/.config/jd4/config.yaml && \
    rm -rf /tmp/jd4
CMD bash -c "source /venv/bin/activate && \
             python3 -m jd4.daemon"
