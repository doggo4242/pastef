FROM alpine:edge
RUN mkdir /etc/pastef
COPY whitelist.txt /etc/pastef/whitelist.txt
COPY channels.json /etc/pastef/channels.json
COPY requirements.txt /etc/pastef/requirements.txt
ARG TOKEN
ENV TOKEN=$TOKEN
COPY pastef.py /usr/local/bin/pastef
COPY formatter.py /usr/local/bin/formatter.py
RUN apk update
RUN apk --no-cache upgrade
RUN apk --no-cache add gcc python3-dev musl-dev clang-extra-tools npm java-common ruby
RUN npm install --global prettier @prettier/plugin-php
RUN npm cache clean
RUN gem install rufo
RUN python3 -m pip install --upgrade --no-cache-dir pip
RUN python3 -m pip install --no-cache-dir -r /etc/pastef/requirements.txt
RUN apk del gcc python3-dev musl-dev
ENTRYPOINT ["pastef"]
