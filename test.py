import os


def GetBoardPresets(board='b'):
    for root, dirs, files in os.walk("E:/Media/4Chan/" + board):
        if len(dirs) == 0:
            continue
        return dirs

def getBoards():
    a = os.walk("E:/Media/4Chan")
    for i in a:
    	return i[1]


print(getBoards())