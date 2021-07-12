FROM ubuntu:20.04

# basic libs
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y sudo vim wget curl git file unzip xz-utils
RUN apt-get install -y build-essential zlib1g-dev gcc make

# locale
RUN apt-get install -y locales
RUN locale-gen ja_JP.UTF-8

# python
RUN apt-get install -y python3 python3-pip
ENV PYTHONIOENCODING "utf-8"
WORKDIR /usr/local/bin/
RUN ln -s `which python3` python
RUN ln -s `which pip3` pip

# mecab
RUN apt-get install -y mecab libmecab-dev
RUN apt-get install -y mecab-ipadic-utf8 unidic-mecab

# mecab-ipadic-NEologd
WORKDIR /usr/local/src
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y

# mecab-unidic-NEologd
WORKDIR /usr/local/src
RUN git clone --depth 1 https://github.com/neologd/mecab-unidic-neologd.git
RUN cd mecab-unidic-neologd && ./bin/install-mecab-unidic-neologd -n -y

# mecab-naist-jdic
WORKDIR /usr/local/src
RUN wget https://ja.osdn.net/projects/naist-jdic/downloads/53500/mecab-naist-jdic-0.6.3b-20111013.tar.gz
RUN tar xzvf mecab-naist-jdic-0.6.3b-20111013.tar.gz
RUN cd mecab-naist-jdic-0.6.3b-20111013 && \
    ./configure --with-charset=utf8 --with-mecab-config=/usr/bin/mecab-config && \
    make && make install

# mecabrc
WORKDIR /etc
RUN sed -i -e 's/dicdir = .*/dicdir = \/usr\/lib\/x86_64-linux-gnu\/mecab\/dic\/mecab-ipadic-neologd/g' mecabrc
RUN cp mecabrc /usr/local/etc/mecabrc

# python libs
RUN pip install --upgrade pip
RUN pip install mecab-python3

# python libs (spaCy & GiNZA)
RUN pip install spacy ginza
RUN python -m spacy download ja_core_news_sm
RUN python -m spacy download ja_core_news_md
RUN python -m spacy download ja_core_news_lg

WORKDIR /app

COPY ./ /app

RUN pip install -r requirements.txt

CMD ["python", "flask_app.py"]