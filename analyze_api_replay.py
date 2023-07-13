#!/bin/env python3

import json
import argparse
from statistics import mean

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", help="replay input json")
    args = parser.parse_args()

    with open(args.datafile, "rb") as f:
        data = json.load(f)

    empty_md5 = 'd751713988987e9331980363e24189ce'

    # get the total request time
    total_time = 0    
    avg_md5 = {}
    urls_md5 = {m: len(data[m]) for m in data}
    md5_calls = {}
    for m in data:
        md5_calls[m] = 0
        for u in data[m]:
            total_time += sum(data[m][u])            
            avg_md5[m] = mean(data[m][u])
            md5_calls[m] += len(data[m][u])

    print(f"{total_time} seconds were spent in requests")
    print(f"{len(list(data.keys()))} distinct responses found")
    # get the information about empty calls
    print(f"{len(data[empty_md5])} urls returned an empty list")
    ecalls = 0
    etime = 0
    for u in data[empty_md5]:
        ecalls += len(data[empty_md5][u])
        etime += sum(data[empty_md5][u])
    print(f"{ecalls} calls returned an empty list")
    print(f"{etime} seconds spent retrieving empty lists")
    for l in (25, 20, 15, 10, 5, 1):
        ucalls=len([m for m in md5_calls if md5_calls[m] > l])
        
        print(f"{ucalls} MD5s retrieved by more than {l} duplicate calls")


if __name__ == "__main__":
    main()