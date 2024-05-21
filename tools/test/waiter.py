#!/bin/env python3

import time
import os
import sys

def main():
    with open(f"/tmp/waiter.log", "a") as f:
        f.write(f"starting at {time.time()}, ppid: {os.getppid()}, args: {sys.argv}\n")        
        time.sleep(10)
        exit(255)

if __name__ == "__main__":
    main()