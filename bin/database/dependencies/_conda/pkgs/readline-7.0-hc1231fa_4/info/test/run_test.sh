

set -ex



test -f ${PREFIX}/lib/libreadline.a
test -f ${PREFIX}/lib/libreadline.dylib
test -f ${PREFIX}/lib/libhistory.a
test -f ${PREFIX}/lib/libhistory.dylib
exit 0
