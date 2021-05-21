FROM doggo4242/pastef:latest
ARG token
ENV TOKEN ${token}
COPY whitelist.txt /etc/pastef/whitelist.txt
COPY channels.json /etc/pastef/channels.json
COPY requirements.txt /etc/pastef/requirements.txt
COPY pastef.py /usr/local/bin/pastef
COPY formatter.py /usr/local/bin/formatter.py
RUN apk update
RUN apk --no-cache upgrade
RUN apk --no-cache add gcc python3-dev musl-dev
RUN python3 -m pip install --upgrade --no-cache-dir pip
RUN python3 -m pip install --no-cache-dir -r /etc/pastef/requirements.txt
RUN apk del gcc python3-dev musl-dev
ENTRYPOINT ["pastef"]
