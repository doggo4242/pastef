# pastef- a formatting/pastebinning discord bot

## Usage
React with a paperclip to pastebin any codeblocks. React with any pen emoji to format and pastebin the codeblocks.

## Install

Clone the repo, then create the required config files in the same directory as the Dockerfile.

`token.txt`: contains your bot account token

`whitelist.txt`: contains role ids of roles whose messages should be ignored by the bot. Separate ids with newlines.

`channels.json`: contains a dict of json keys/values where the key is the channel id (as a string) of the channels the bot should be active in, and the value is the backup language specifier (accepts discord codeblock specifiers). Put "" for the key if you would not like to use backup language specification.

Build the image:

```
docker build -t pastef .
```

Run the container:

```
docker run -d=true pastef
```

Done :)

## Editing the config

After editing the config, you will need to rebuild the image.

```
docker build --no-cache -t pastef .
```

Then run the container:

```
docker run -d=true pastef
```

## Troubleshooting

If something isn't working, it's most likely a configuration error. Run the container without the `-d=true` flag to see which file is causing the error. If the issue seems unrelated to the configuration, report it on the issues page.
