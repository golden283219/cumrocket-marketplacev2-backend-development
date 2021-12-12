FROM ruby:2.5
RUN apt-get update -qq && apt-get install -y nodejs
WORKDIR /app

ADD Gemfile /myapp/Gemfile
ADD Gemfile.lock /myapp/Gemfile.lock

COPY ./src/ /app/

RUN bundle install
RUN npm install

ADD ./requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir -p /static/
WORKDIR /app