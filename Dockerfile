FROM alpine:latest
RUN apk update
RUN apk --no-cache upgrade
RUN apk --no-cache add gcc python3-dev musl-dev binutils go cmake make alpine-sdk git g++ curl rust yaml-cpp-dev ninja wget
RUN mkdir /github/workspace/formatters
RUN cp $(which rustfmt) /github/workspace/formatters
RUN cp $(which gofmt) /github/workspace/formatters
RUN go get -u github.com/klauspost/asmfmt/cmd/asmfmt
RUN cp $(which asmfmt) /github/workspace/formatters
RUN "curl -s https://api.github.com/repos/tweag/ormolu/releases/latest | grep ormolu-Linux | cut -d : -f 2,3 | tr -d \" | wget -qi -O /github/workspace/formatters/ormolu -"
RUN cd /github/workspace
RUN git clone https://Koihik/LuaFormatter.git
RUN cd LuaFormatter
RUN git submodule update --init --recursive
RUN cmake -GNinja .
RUN ninja -j20
RUN cp lua-format /github/workspace/formatters
RUN cd /github/workspace
RUN rm -rf LuaFormatter
RUN "curl -s https://api.github.com/repos/pinterest/ktlint/releases/latest | grep ktlint | cut -d : -f 2,3 | tr -d \" | wget -qi -O /github/workspace/formatters/ktlint -"
RUN tar -czvf formatters.tar.gz formatters
RUN rm -rf formatters
