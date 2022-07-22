from bisect import bisect
import netaddr
import re
import pandas as pd
import time
ips = pd.read_csv("ip2location.csv")
def lookup_region(ip_address):
    ip_address = re.sub('[^0-9.]','0',ip_address)
    ip = int(netaddr.IPAddress(ip_address))
    idx = bisect(ips['low'],ip)
    return ips.iloc[idx-1]['region']

if __name__ == "__main__":
    while True:
        with open('./logs/access.log') as logfile:
            string = logfile.read()
            stringlist = string.split('\n')
        for i in range(len(stringlist)):
            a = re.findall(r"^\d+\.\d+\.\d+\.\d+",stringlist[i])
            if len(a)!=0:
                stringlist[i] = stringlist[i].replace(a[0],lookup_region(a[0]))
        result = ""
        for i in stringlist:
            result = result+i+"\n"
        with open('./logs/accessloc.log','w') as loc:
            loc.write(result)
        time.sleep(3600)
    
    