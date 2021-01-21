FROM pastef:latest
COPY token.txt /etc/pastef/token.txt
COPY whitelist.txt /etc/pastef/whitelist.txt
COPY channels.json /etc/pastef/channels.json
CMD ["pastef"]
