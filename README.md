# pastef
A code formatting and pastebinning discord bot. Formats codeblocks and/or uploads them to a paste service when a message is reacted to with any pen emoji (formats) or a paperclip emoji (pastebins). 

# Usage
Download the Dockerfile, then create the required config files in the same directory as the Dockerfile.

`token.txt`: contains your bot account token

`whitelist.txt`: contains role ids of roles whose messages should be ignored by the bot.

`channels.json`: contains a dict of json keys/values where the key is the channel id (as a string) of the channels the bot should be active in, and the value is the backup language specifier (accepts discord codeblock specifiers). Put "" for the key if you would not like to use backup language specification.

Build the image:

```
docker build -t pastef
```

Done :)

Formatter supports everything clang-format and prettier support, as well as kotlin, python, php, rust, haskell, lua, asm, go, and ruby.

# TODO

# Credits
Thanks to @PHOENiX for the regex

Thanks to @m1lkweed for the name

Formatters used:

[clang-format](https://clang.llvm.org/docs/ClangFormat.html)

[prettier](https://prettier.io)

[yapf](https://github.com/google/yapf)

[ktlint](https://github.com/pinterest/ktlint)

[rustfmt](https://github.com/rust-lang/rustfmt)

[ormolu](https://github.com/tweag/ormolu)

[LuaFormatter](https://github.com/Koihik/LuaFormatter)

[asmfmt](https://github.com/klauspost/asmfmt)

[gofmt](https://golang.org/cmd/gofmt/)

[rufo](https://github.com/ruby-formatter/rufo)
