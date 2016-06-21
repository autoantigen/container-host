import sys, re, os, json, subprocess

def insert(ipaddress, hostname):    
    outputfile = open('/etc/hosts', 'a')
    entry = "\n" + ipaddress + "\t" + hostname + "\n"
    outputfile.writelines(entry)
    outputfile.close()
    print "==========================================="
    print "inserted new line:", ipaddress, hostname
    print "==========================================="

def exists(hostname):   
    f = open('/etc/hosts', 'r')
    hostfiledata = f.readlines()
    f.close()
    for line in hostfiledata:
        if hostname in line:
            return True
    return False

def host(container):
    m2host = subprocess.Popen(['docker', 'inspect', container], stdout=subprocess.PIPE)
    m2 = m2host.stdout.read()
    p_json = json.loads(m2)
    newIp = p_json[0]["NetworkSettings"]["IPAddress"]
    return newIp

def update(ipaddress, hostname):
    f = open('/etc/hosts', 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        if hostname not in line:
           continue
        else:
           f = open('/etc/hosts', 'r')
           contents = f.read()
           f.close()  
           c = contents.replace(line, "\n" + ipaddress + "\t" + hostname + "\n")
	   print "==========================================="
           print "old line:", line
           f = open('/etc/hosts', 'w')
           f.write(c)
           f.close()          
           print "changed with new line:", ipaddress, hostname
	   print "==========================================="

def main():
    args = sys.argv
    if len(args) != 3:
        print "================================================================"
        print('usage: sudo python route.py nginx_container_name hostname' )
        print "================================================================"
        sys.exit(2)
    container = str(args[-2])
    hostname = args[-1]    
    
    ipaddress = host(container)
    if exists(hostname):
        update(ipaddress, hostname)  
    else:
        insert(ipaddress, hostname)

main()
