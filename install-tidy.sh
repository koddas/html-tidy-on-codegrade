#!/bin/sh

# Check https://github.com/htacg/tidy-html5/releases for the latest release
TIDY_VERSION=5.7.28

set -e

tmp=$(mktemp -d)

(
    cd $tmp
    wget -O tidy.zip https://github.com/htacg/tidy-html5/archive/refs/tags/$TIDY_VERSION.zip
    unzip tidy.zip

    cd tidy-html5-$TIDY_VERSION/build/cmake
    cmake ../.. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIB:BOOL=OFF
    make && sudo make install

    cd && rm -rf $tmp
)
