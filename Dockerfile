FROM ubuntu:14.04
MAINTAINER judy.programer@gmail.com
EXPOSE 5000

RUN mkdir /usr/app
WORKDIR /usr/app
ADD requirements.txt ./

# Dependencies we just need for building phantomjs
ENV buildDependencies\
  wget unzip python build-essential g++ flex gperf\
  nodejs npm ruby perl libsqlite3-dev libssl-dev libpng-dev

# Dependencies we need for running phantomjs
ENV phantomJSDependencies\
  libicu-dev libfontconfig1-dev libjpeg-dev libfreetype6 openssl

# Installing phantomjs
RUN \
    # Installing dependencies
    apt-get update -yqq \
&&  apt-get install -fyqq ${buildDependencies} ${phantomJSDependencies} --fix-missing \
    # Downloading src, unzipping & removing zip
&&  mkdir phantomjs \
&&  cd phantomjs \
&&  wget https://github.com/pocketjoso/phantomjs2/archive/master.zip \
&&  unzip master.zip \
&&  mv phantomjs2-master phantomjs2 \
&&  rm -rf /phantomjs/phantomjs2-master.zip \
&&  cd phantomjs2/ \
&&  npm install -g phantomjs2 \
&&  ls -A | grep -v bin | xargs rm -rf \
    # Symlink phantom so that we are able to run `phantomjs`
&&  ln -s /phantomjs/phantomjs2/bin/phantomjs /usr/local/share/phantomjs \
&&  ln -s /phantomjs/phantomjs2/bin/phantomjs /usr/local/bin/phantomjs \
&&  ln -s /phantomjs/phantomjs2/bin/phantomjs /usr/bin/phantomjs \
    # Removing build dependencies, clean temporary files
&&  apt-get purge -yqq ${buildDependencies} \
&&  apt-get autoremove -yqq \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    # Checking if phantom works
&&  phantomjs -v

CMD \
    echo "phantomjs binary is located at /phantomjs/phantomjs2/bin/phantomjs"\
&&  echo "just run 'phantomjs' (version `phantomjs -v`)"

RUN pip install -r requirements.txt
ADD . .
