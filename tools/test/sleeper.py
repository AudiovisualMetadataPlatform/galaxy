#!/bin/env python3

import time
import os
import sys

def main():
    with open(f"/tmp/sleeper-{os.getpid()}.log", "w") as f:
        f.write(f"starting at {time.time()}, ppid: {os.getppid()}, args: {sys.argv}\n")
        while True:
            f.write(f"continuing at {time.time()}, ppid: {os.getppid()}\n")
            f.flush()
            time.sleep(10)

if __name__ == "__main__":
    main()