FROM pypy:3.7-buster
LABEL maintainer="Jens Preussner <jens@factsforfriends.de>"

COPY . /opt/fff-scrapy

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN \
    cd /opt/fff-scrapy && \
    pip install -r requirements.txt

WORKDIR /opt/fff-scrapy

CMD ["scrapy"]