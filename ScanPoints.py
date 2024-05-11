
import random
import time

class ScanPoints:
    def __init__(self, bombNum, mapCellNum, limitTime):
        # 默认控制参数
        self.bombNum = bombNum                    # 地雷数
        self.mapCellNum = mapCellNum              # 格子数
        self.limitTime = limitTime                # 限制游戏结束时间

        # 系统参数
        self.startUtcTime = 0  # 开始游戏时间戳
        self.remainTime = 0    # 剩余时间
        self.bombPositionList = []
        self.bombMapList = []
        self.percentMapList = []
        self.displayMapList = []
        self.markPositionList = []

    # 开始计时
    def recordStartTime(self):
        self.startUtcTime = self.getNowUtc()

    # 设置难度
    def setLevel(self, level):
        if level <= 0:
            level = 5
        # 设置单元格数量对应比例的炸弹数
        self.bombNum = self.mapCellNum * self.mapCellNum / level

    # 获取当前utc时间
    def getNowUtc(self):
        return time.time()

    # 获取随机整形
    def randomInt(self, startidx, endidex):
        return random.randint(startidx, endidex)

    # 计算游戏剩余时间
    def getRemainTime(self):
        useTime = self.getNowUtc() - self.startUtcTime
        self.remainTime = self.limitTime - useTime
        minute = int(self.remainTime / 60)
        second = int(self.remainTime % 60)
        strLimitTime = str(minute) + ":" + str(second)
        return strLimitTime

    # 剩余时间不足结束判断
    def isTimeOut(self):
        if self.remainTime <= 0 :
            return True
        return False

    # 胜利判断
    def isWin(self):
        if len(set(self.bombPositionList) - set(self.markPositionList)) == 0:
            return True
        return False

    # 产生地雷
    def generateBomb(self):
        while True:
            if len(self.bombPositionList) < self.bombNum:
                position = (self.randomInt(0, self.mapCellNum-1), self.randomInt(0, self.mapCellNum-1))
                if position not in self.bombPositionList:
                    self.bombPositionList.append(position)
            else:
                break

    # 生成地图
    def genarateMap(self):
        # 生成地雷
        self.generateBomb()

        # 生成地图
        for i in range(self.mapCellNum):
            tempbombListMap = []
            tempDisplayList = []
            for j in range(self.mapCellNum):
                tempDisplayList.append("#")
                if (i, j) in self.bombPositionList:
                    tempbombListMap.append(1)
                else:
                    tempbombListMap.append(0)
            self.bombMapList.append(tempbombListMap)
            self.displayMapList.append(tempDisplayList)

        # 计算地雷分布概率
        self.caculatePercentage()

    # 计算地雷分布概率
    def caculatePercentage(self):
        for i in range(self.mapCellNum):
            tempList = []
            for j in range(self.mapCellNum):
                percentage = 0
                if self.bombMapList[i][j] == 1:
                    tempList.append("*")
                    continue

                if i - 1 >= 0 and j - 1 >= 0:
                    percentage = percentage + self.bombMapList[i-1][j-1]
                if i - 1 >= 0:
                    percentage = percentage + self.bombMapList[i-1][j]
                if i - 1 >= 0 and j + 1 < self.mapCellNum:
                    percentage = percentage + self.bombMapList[i-1][j+1]

                if j - 1 >= 0:
                    percentage = percentage + self.bombMapList[i][j-1]
                if j + 1 < self.mapCellNum:
                    percentage = percentage + self.bombMapList[i][j+1]
                    
                if i + 1 < self.mapCellNum and j - 1 >= 0:
                    percentage = percentage + self.bombMapList[i+1][j-1]
                if i + 1 < self.mapCellNum:
                    percentage = percentage + self.bombMapList[i+1][j]
                if i + 1 < self.mapCellNum and j + 1 < self.mapCellNum:
                    percentage = percentage + self.bombMapList[i+1][j+1]
                tempList.append(str(percentage))
    
            self.percentMapList.append(tempList)

    # 处理点击位置所有周边格子
    def processClickCellAround(self, positionX, positionY):
        for direction in ["up", "upRight", "right", "downRight", "down", "downLeft", "left", "upleft"]:
            self.processClickCell(positionX, positionY, direction)

    # 显示点击后的区域
    def processClickCell(self, positionX, positionY, position):
        displayZero = False

        # 当点击位置概率为0时,需要看其他8个方位是否有为0的格子,如果有则继续递归直到找到不为0的格子
        if self.percentMapList[positionX][positionY] == '0':
            if position == "up" and positionX > 0:
                self.processClickCell(positionX-1, positionY, position)
            elif position == "upRight" and positionX > 0 and positionY < self.mapCellNum-1:
                self.processClickCell(positionX-1, positionY+1, position)
            elif position == "right" and positionY < self.mapCellNum-1:
                self.processClickCell(positionX, positionY+1, position)
            elif position == "downRight" and positionX < self.mapCellNum-1 and positionY < self.mapCellNum-1:
                self.processClickCell(positionX+1, positionY+1, position)
            elif position == "down" and positionX < self.mapCellNum-1:
                self.processClickCell(positionX+1, positionY, position)
            elif position == "downLeft" and positionX < self.mapCellNum-1 and positionY > 0:
                self.processClickCell(positionX+1, positionY-1, position)
            elif position == "left" and positionY > 0:
                self.processClickCell(positionX, positionY-1, position)
            elif position == "upleft" and positionX > 0 and positionY > 0:
                self.processClickCell(positionX-1, positionY-1, position)
            else:
                displayZero = True

        # 当点击的位置没有标记的时候才更新值
        if (positionX, positionY) not in self.markPositionList:
            if displayZero:
                self.displayMapList[positionX][positionY] = "0"
            else:
                self.displayPercent(positionX, positionY)

    # 显示百分比
    def displayPercent(self, positionX, positionY):
        if self.percentMapList[positionX][positionY] != '*':
            self.displayMapList[positionX][positionY] = self.percentMapList[positionX][positionY]

    # 点击某格
    def clickCell(self, positionX, positionY):
        isOver = False
        
        # 如果是地雷直接结束
        if (positionX, positionY) in self.bombPositionList:
            isOver = True
        else:
            self.processClickCellAround(positionX, positionY)
        
        return isOver

    # 标记格子
    def markCell(self, positionX, positionY):
        if self.displayMapList[positionX][positionY] == "#":
            self.displayMapList[positionX][positionY] = "@"
            self.markPositionList.append((positionX, positionY))
        elif self.displayMapList[positionX][positionY] == "@":
            self.displayMapList[positionX][positionY] = "#"
            self.markPositionList.remove((positionX, positionY))