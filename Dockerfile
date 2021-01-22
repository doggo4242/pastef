FROM doggo4242/pastef:latest
COPY token.txt /etc/pastef/token.txt
COPY whitelist.txt /etc/pastef/whitelist.txt
COPY channels.json /etc/pastef/channels.json
COPY pastef.py /usr/local/bin/pastef
COPY formatter.py /usr/local/bin/formatter.py
CMD ["pastef"]
