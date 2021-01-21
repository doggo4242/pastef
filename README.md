# pastef
A code formatting and pastebinning discord bot. Formats codeblocks and/or uploads them to a paste service when a message is reacted to with any pen emoji (formats) or a paperclip emoji (pastebins). 

# Usage
Docker image coming soon.
Formatter supports everything clang-format and prettier support, as well as kotlin, python, php, rust, haskell, lua, asm, go, and ruby.

# TODO
Prevent double reactions

Add tph-specific formatter guessing if none is available.

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
