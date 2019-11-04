#!/bin/bash

# Prevent running ldconfig when cross-compiling
if [[ "${BUILD}" != "${HOST}" ]]; then
  echo "#!/usr/bin/env bash" > ldconfig
  chmod +x ldconfig
  export PATH=${PWD}:$PATH
fi

./configure --prefix=${PREFIX}   \
            --build=${BUILD}     \
            --host=${HOST}       \
            --enable-threadsafe  \
            --enable-shared=yes  \
            --enable-readline    \
            --enable-editline    \
            --disable-readline   \
            CFLAGS="${CFLAGS} -I${PREFIX}/include" \
            LDFLAGS="${LDFLAGS} -L${PREFIX}/lib"
make -j${CPU_COUNT} ${VERBOSE_AT}
make check
make install

rm -rf  ${PREFIX}/share
