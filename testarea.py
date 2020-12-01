import cv2
import numpy as np
#import pygame
import math


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

def astar(maze, start, end, col, row):
    start_node = Node(None, start)
    end_node = Node(None, end)

    start_node.g = start_node.h = start_node.f = 0
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        print(len(open_list))
        img = tempimg.copy()
        for item in open_list:
            img[item.position[1],item.position[0],0]= 0
            img[item.position[1],item.position[0],1]= 255
            img[item.position[1],item.position[0],2]= 255
        for item in closed_list:
            img[item.position[1],item.position[0],0]= 0
            img[item.position[1],item.position[0],1]= 0
            img[item.position[1],item.position[0],2]= 255
        cv2.imshow('image',img)
        cv2.waitKey(1)
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        del open_list[current_index]
        closed_list.append(current_node)

        if current_node.position[0] == end_node.position[0] and current_node.position[1] == end_node.position[1]:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        i=0
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])
            i=i+1
            if node_position[0] > col - 1 or node_position[0] < 0 or node_position[1] > row -1 or node_position[1] < 0:
                continue
            if maze[node_position[1]][node_position[0]] != 0:
                continue
            checklist = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            checklist.extend([(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2)])
            checklist.extend([(-2,  2), (-1,  2), (0,  2), (1,  2), (2,  2)])
            checklist.extend([(-2,  -1), (-2,  0), (-2,  1)])
            checklist.extend([( 2,  -1), ( 2,  0), ( 2,  1)])
            cnt = True
            for checkpos in checklist:
                newcheckpos = (node_position[0] + checkpos[0],node_position[1] + checkpos[1])
                if newcheckpos[0] > col - 1 or newcheckpos[0] < 0 or newcheckpos[1] > row-1 or newcheckpos[1] < 0:
                    cnt = False
                    break
                if maze[newcheckpos[1]][newcheckpos[0]] != 0:
                    cnt = False
                    break
            if cnt == False:
                continue
            new_node = Node(current_node, node_position)
            cnt = False
            for closed_child in closed_list:
                if new_node.position[0] == closed_child.position[0] and new_node.position[1] == closed_child.position[1]:
                    cnt = True
                    break
            if cnt == True:
                continue
            new_node.g = current_node.g +  np.sqrt(((current_node.position[0] - new_node.position[0]) ** 2) + ((current_node.position[1] - new_node.position[1]) ** 2))
            new_node.h = np.sqrt(((new_node.position[0] - end_node.position[0]) ** 2) + ((new_node.position[1] - end_node.position[1]) ** 2))
            new_node.f = new_node.g + new_node.h
            cnt=False
            for open_node in open_list:
                if new_node.position[0] == open_node.position[0] and new_node.position[1] == open_node.position[1]:
                    if new_node.g < open_node.g:
                        open_node.parent = new_node.parent
                        open_node.f = new_node.f
                        open_node.g = new_node.g
                        open_node.h = new_node.h
                    cnt = True
                    break
            if cnt == True:
                continue
            open_list.append(new_node)


maze = []
img = cv2.imread('mymap.pgm',1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
test = np.copy(gray)
shape = np.shape(gray)
row = int(shape[0])
col = int(shape[1])

for i in range (row):       
    line = []
    for t in range(col):
        if gray[i,t] >= 250:      
            gray[i,t] = 0
            test[i,t] = 255                
            line.append(0)
        else:
            gray[i,t] = 1
            test[i,t] = 0
            line.append(1)
    maze.append(line)
        


start = (210,248)
end = (160,426)

tempimg = img.copy()

path = astar(maze, start, end, col, row)

for i in range (len(path)):
    piksel = path[i]
    img[piksel[1],piksel[0],0]= 0
    img[piksel[1],piksel[0],1]= 255
    img[piksel[1],piksel[0],2]= 0

cv2.imshow('image',img)
cv2.waitKey(0)
    

    
          


