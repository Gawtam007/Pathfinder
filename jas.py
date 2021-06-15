# ED3170 - Pathfinding Project  
# By Jaswanth, Gokul and Gawtam

import sys
from PyQt5 import QtWidgets, uic
import time
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt, QTimer
from PyQt5 import QtCore
from FrontEnd import Ui_Dialog

sys.setrecursionlimit(10**6)
tym, outerIter, ROW, COL, button = 0, 0, 52, 32, 0
startPos, endPos, obstaclePos, path = [-1, -1], [-1, -1], [], []

class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

class MainWindow(QtWidgets.QMainWindow, Ui_Dialog):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.createGraphicsView()

        # linking the buttons with the respective functions 
        self.startb.pressed.connect(self.startMode)          
        self.endb.pressed.connect(self.endMode)
        self.obsb.pressed.connect(self.obstacleMode)
        self.clrScrb.pressed.connect(self.clearScreenMode)
        self.clrObsb.pressed.connect(self.clearObstaclesMode)
        self.clrPathb.pressed.connect(self.call_astar)
        
    
    def createGraphicsView(self):
        self.scene = QGraphicsScene()
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.drawGrid()
        self.graphicsView.viewport().installEventFilter(self)

    # funtion to draw 53 x 33 grid lines  
    def drawGrid(self):

        self.scene.setBackgroundBrush(Qt.darkCyan)
        for x in range(0, 1041, 20):
            self.scene.addLine(x, 0, x, 640, QPen(Qt.white))
        for y in range(0, 641, 20):
            self.scene.addLine(0, y, 1040, y, QPen(Qt.white))
        self.graphicsView.setScene(self.scene)
   
    # functions to check overlaps
    def overlapCheck(self, a, b):

        global startPos, endPos, obstaclePos
        for lst in obstaclePos:
            if lst == [a, b]:
                return True
        if startPos == [a, b]:
            return True
        elif endPos == [a, b]:
            return True
        return False

    def obsOverlapCheck(self, a, b):

        global startPos, endPos, obstaclePos
        for lst in obstaclePos:
            if lst == [a, b]:
                return True
        return False

    #region Funtion to access nodes
    def startMode(self):
        global button
        button = 0  
    def endMode(self):
        global button
        button = 1
    def obstacleMode(self):
        global button
        button = 2
    #endregion

    # function to reset start, end and obstacle nodes
    def clearScreenMode(self):
        self.scene.clear()
        global startPos, endPos, obstaclePos
        startPos = [-1, -1]
        endPos = [-1, -1]
        obstaclePos = []
        self.drawGrid()
      # Function to clear obstacles
   
   # function to check 
    def clearObstaclesMode(self):
        self.scene.clear()
        global obstaclePos
        obstaclePos = []

        self.drawGrid()
        brush = QBrush()
        brush.setColor(Qt.red)
        brush.setStyle(Qt.SolidPattern)
        borderColor = Qt.black
        if not startPos[0] == -1:
            self.scene.addRect(QRectF(startPos[0] * 20, startPos[1] * 20, 20, 20), borderColor, brush)
        if not endPos[0] == -1:
            brush.setColor(Qt.green)
            self.scene.addRect(QRectF(endPos[0] * 20, endPos[1] * 20, 20, 20), borderColor, brush)
    
    # Function to call the a_star algortihm 
    def call_astar(self):
        path = self.aStarAlgo()
        self.paintPath(path)
        print("No of Interation : ", outerIter)
    
    #  H calculation with Manhattan distance (distance between two points measured along axes at right angles)
    def nodeDist(self, node1, node2):
        return abs(node1.position[0] - node2.position[0]) + abs(node1.position[1] - node2.position[1])
    
    # Function to find the shortest path using A* algorithm
    def aStarAlgo(self):
        global startPos, endPos, path, outerIter, tym

        maxIter = 10**6  # Maximum allowed iterations 


        if startPos[0] != -1 and endPos != -1:

            startNode = Node(None, startPos)
            endNode = Node(None, endPos)
            openList = []
            closeList = []
            openList.append(startNode)

            movement = [[-1, 0], [0, -1], [1, 0], [0, 1]]

            while len(openList) > 0:

                cont = 0          
                currNode = openList[0]
                currIndex = 0

            

                for index, item in enumerate(openList):
                    outerIter += 1
                    
                    if item.f < currNode.f:
                        currNode = item
                        currIndex = index

                    # painting the nodes to visualise path
                    brush = QBrush()
                    brush.setColor(Qt.cyan)
                    brush.setStyle(Qt.SolidPattern)
                    borderColor = Qt.black
                    self.scene.addRect(QRectF(currNode.position[0] * 20, currNode.position[1] * 20, 20, 20), borderColor, brush)

                QApplication.processEvents()

                if outerIter >= maxIter:
                    print(" Max iterations reached !!! ")
                    path = []
                    return path

                # removing the current index out of the openList to avoid rechecking 
                openList.pop(currIndex)

                # adding the current node to closeList
                closeList.append(currNode)

                if currNode == endNode:
                    path = []
                    current = currNode

                    # reading the current node from 
                    while current is not None:
                        path.append(current.position)
                        current = current.parent
                    return path[::-1]

                children = []

                for move in movement:
                    nodePos = [currNode.position[0] + move[0], currNode.position[1] + move[1]]

                    if nodePos[0] > ROW - 1 or nodePos[0] < 0 or nodePos[1] > COL - 1 or nodePos[1] < 0:
                        continue

                    if Node(currNode, nodePos) in closeList:
                        continue

                    if self.obsOverlapCheck(nodePos[0], nodePos[1]):
                        continue

                    newNode = Node(currNode, nodePos)

                    children.append(newNode)

                for child in children:
                    for closeChild in closeList:
                        if child == closeChild:
                            cont = 1

                    if cont == 1:
                        cont = 0
                        continue

                    child.g = currNode.g +  1
                    child.h = self.nodeDist(endNode, child)
                    child.f = child.g + child.h

                    for openNode in openList:
                        if child == openNode and child.g >= openNode.g:
                            cont = 1

                    if cont == 1:
                        cont = 0
                        continue

                    openList.append(child)
    
    # Funtion to paint the 
    def paintPath(self, path):
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        borderColor = Qt.black
        if path == None:
            print("NO PATH")
        else:
            for i in path:
                self.scene.addRect(QRectF(i[0] * 20, i[1] * 20, 20, 20), borderColor, brush)

    # 
    def eventFilter(self, source, event):
        clrBrush = QBrush()
        clrBrush.setColor(Qt.darkCyan)
        clrBrush.setStyle(Qt.SolidPattern)
        clrBorderColor = Qt.white
        borderColor = Qt.black

        if (event.type() == QtCore.QEvent.MouseMove and source is self.graphicsView.viewport()):
            if button == 2:
                pos = event.pos()
                brush = QBrush()
                brush.setColor(Qt.gray)
                brush.setStyle(Qt.SolidPattern)
                x = (pos.x() // 20)
                y = (pos.y() // 20)
                if not self.overlapCheck(x, y):
                    self.scene.addRect(QRectF(x * 20, y * 20, 20, 20), borderColor, brush)
                    obstaclePos.append([x, y])

        if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.graphicsView.viewport()):
            if button == 0:
                pos = event.pos()
                brush = QBrush()
                brush.setColor(Qt.red)
                brush.setStyle(Qt.SolidPattern)
                x = (pos.x() // 20)
                y = (pos.y() // 20)
                if not self.overlapCheck(x, y):
                    self.scene.addRect(QRectF(x * 20, y * 20, 20, 20), borderColor, brush)
                    if not startPos[0] == -1:
                        self.scene.addRect(QRectF(startPos[0] * 20, startPos[1] * 20, 20, 20), clrBorderColor, clrBrush)
                    startPos[0] = x
                    startPos[1] = y

            elif button == 1:
                pos = event.pos()
                brush = QBrush()
                brush.setColor(Qt.green)
                brush.setStyle(Qt.SolidPattern)
                x = (pos.x() // 20)
                y = (pos.y() // 20)
                if not self.overlapCheck(x, y):
                    self.scene.addRect(QRectF(x * 20, y * 20, 20, 20), borderColor, brush)
                    if not endPos[0] == -1:
                        self.scene.addRect(QRectF(endPos[0] * 20, endPos[1] * 20, 20, 20), clrBorderColor, clrBrush)
                    endPos[0] = x
                    endPos[1] = y

            elif button == 2:
                pos = event.pos()
                brush = QBrush()
                brush.setColor(Qt.gray)
                brush.setStyle(Qt.SolidPattern)
                x = (pos.x() // 20)
                y = (pos.y() // 20)
                if not self.overlapCheck(x, y):
                    self.scene.addRect(QRectF(x * 20, y * 20, 20, 20), borderColor, brush)
                    obstaclePos.append([x, y])

        return QtWidgets.QWidget.eventFilter(self, source, event)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
