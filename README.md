# 4ChanPlunderer
Program for downloading images and videos from 4Chan with filters 
###### Useful if you regularly visit specific threads, and want to automate that process

- Use multiple whitelist, blacklist filters
- Organizes folders by board > filter title
- Can run indefinitely

## Setup
1. ```pip install requests``` 
2. ```python console.py```
3. Follow the command prompts! :3 

## Roadmap 
#### There was at one point a functional gui using tkinter, but that had it's limitations so I'll eventually do a port on winforms
###### (In order of importance)
- Ability to toggle different filters for console
- Stats page that displays a line graph of downloads 
- When given blank entry add blank string
- Save button will show the recently added checkboxes
- Upon setup user can save multiple queries at a time before pressing back
- Tick box, press save, get error, and have that checkbox save what was ticked
- Implement settings tab - Unstarted
- Add a menu to delete, save, or skip images presented to the user - Unstarted



## Completed
- Implement tab to show console
- Allow user to toggle which selections will be used
- Get start/stop to work while downloading images
- Safely stop program avoiding half-downloaded images
