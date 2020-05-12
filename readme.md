```
                    __  __       
   ______________  / /_/ /___  __
  / ___/ ___/ __ \/ __/ __/ / / /
 (__  ) /__/ /_/ / /_/ /_/ /_/ / 
/____/\___/\____/\__/\__/\__, /  
                        /____/  
```
# Scotty - Stream Files over LAN using WebSockets
Scotty is an application you can use to transfer large files over LAN (without using any internet)
and without needing any sort of pen-drive or hard disk. Since it is written in python, it is
cross-platform provided that you have `python` and `pip` working. Say good-bye to that nasty search
for pendrives and to struggling to send that one file over email urgently!

## Features
- [x] Send and Recieve files without using internet 
- [ ] Send one file to multiple clients
- [ ] Send multiple files to one client

## Depenedcies
* Python > 3.6
* Rich (text formatting library)
* simple-term-menu (menu in terminal)

## Roadmap
1. Send Files to Fixed Client
2. Recieve Files from Fixed Client
3. Full Duplex - being able to both send and recieve files with a fixed client
4. Multiplex -  Be able to change client and send Files to different clients in the same session
