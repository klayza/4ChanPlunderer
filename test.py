title = "other"
board = "g"
whitelist = "phone", "wallpaper"
blacklist = "hate", "linux"

custom = [title, board, [item for item in whitelist], [item for item in blacklist]]
print(custom)