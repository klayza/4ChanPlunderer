# 4ChanPlunderer
Program for downloading images and videos from 4Chan with filters 
###### Useful if you regularly visit specific threads, and want to automate that process

- Use multiple whitelist, blacklist filters
- Organizes folders by board > filter title
- Can run indefinitely

## Setup
1. ```pip install requests``` 
1. ```pip install matplotlib``` 
2. ```python console.py```
3. Follow the command prompts! :3 

### Silent Mode Setup (Optional)

Use if you want this program to run in the background on startup

1. Edit silent.vbs and link.bat path within their files
2. Copy silent.vbs to ```C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup```

###### Note: This process will be much more simpler in the future, just bear with me lol

## Roadmap 
#### There was at one point a functional gui using tkinter, but that had it's limitations so I'll eventually do a port on winforms
###### (In order of importance)
- Ability to toggle different filters for console
- Save button will show the recently added checkboxes
- Implement settings tab - Started
- Add a menu to delete, save, or skip images presented to the user - Started

## Completed
- Stats page that displays a line graph of downloads 
- Implement tab to show console
- Allow user to toggle which selections will be used
- Get start/stop to work while downloading images
- Safely stop program avoiding half-downloaded images
