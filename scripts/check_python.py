"""
If the current installed Python version is not supported, prints an error
message to stderr and returns 1
"""

import os
import sys

<<<<<<< HEAD
version_string = '.'.join(str(_) for _ in sys.version_info[:3])

msg = """ERROR: Your Python version is: %s
Galaxy is currently supported on Python 2.7 only. To run Galaxy, please
install a supported Python version. If a supported version is already
installed but is not your default, https://galaxyproject.org/admin/python/
contains instructions on how to force Galaxy to use a different version.""" % version_string

msg_beta = """WARNING: Your Python version is: %s
Galaxy is currently supported on Python 2.7 only, support for Python >= 3.4
is still in beta stage. Since you are using a virtual environment, we assume
you are developing or testing Galaxy under Python 3. If not,
install a supported Python version. If a supported version is already
installed but is not your default, https://galaxyproject.org/admin/python/
contains instructions on how to force Galaxy to use a different version.""" % version_string

=======
>>>>>>> refs/heads/release_21.01

def check_python():
<<<<<<< HEAD
    venv = os.getenv('VIRTUAL_ENV')
    if sys.version_info[:2] == (2, 7):
=======
    if sys.version_info[:2] >= (3, 6):
>>>>>>> refs/heads/release_21.01
        # supported
        return
    elif sys.version_info[:2] >= (3, 4) and venv:
        print(msg_beta, file=sys.stderr)
    else:
        version_string = '.'.join(str(_) for _ in sys.version_info[:3])
        msg = """\
ERROR: Your Python version is: %s
Galaxy is currently supported on Python >=3.6 .
To run Galaxy, please install a supported Python version.
If a supported version is already installed but is not your default,
https://docs.galaxyproject.org/en/latest/admin/python.html contains instructions
on how to force Galaxy to use a different version.""" % version_string
        print(msg, file=sys.stderr)
        raise Exception(msg)


if __name__ == '__main__':
    try:
        check_python()
    except Exception:
        sys.exit(1)
