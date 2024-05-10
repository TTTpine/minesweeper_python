import pygame
from ScanPoints import ScanPoints

# 主窗口
class MainWindow():
    def __init__(self):
        # 窗口结束标签
        self.windowOver = False

        # 默认窗口大小
        self.screenWidth = 400
        self.screenheight = 450
        self.windowName = "扫雷"

        # 系统参数
        self.cellsSize = 25     # 单元格长度
        self.mapCellSize = 10    # 地图格子边长
        self.fontHorizontalSize = 7  # 字体水平间距
        self.fontVerticalSize = 3  # 字体垂直间距

        # 定义的颜色部分
        self.DimGreyColor = (105, 105, 105)
        self.BlackColor = (0, 0, 0)
        self.RedColor = (255, 0, 0)
        self.WhiteColor = (255, 255, 255)
        self.LightGrayColor = (211, 211, 211)

        # 用到的颜色
        self.backgroundColor = self.DimGreyColor        # 背景颜色
        self.lineColor = self.BlackColor                # 格子分割线颜色
        self.bombColor = self.BlackColor                # 地雷颜色
        self.clickBombColor = self.RedColor             # 点击的地雷颜色
        self.percentColor = self.WhiteColor             # 百分比颜色
        self.markColor = self.RedColor                  # 标记颜色

    # 重定义窗口内容
    def set_window(self):
        # 扫雷类
        self.ScanPoint = ScanPoints()
        # 设置格子数
        self.ScanPoint.mapCellSize = self.mapCellSize
        self.ScanPoint.setLevel()
        # 设置对应窗口大小
        mapCellSize = self.mapCellSize * self.cellsSize
        self.screenWidth = mapCellSize
        self.screenheight = mapCellSize + self.cellsSize    # 多一格显示内容

    # 初始化窗口
    def init_window(self):
        # 模块初始化
        pygame.init()
        #  创建窗口
        self.screen = pygame.display.set_mode([self.screenWidth,self.screenheight])
        self.font = pygame.font.Font(None, 36)
        # 更改窗口名称
        pygame.display.set_caption(self.windowName)

    # 开始
    def start(self):
        # 重定义窗口内容
        self.set_window()
        # 初始化窗口
        self.init_window()
        # 初始化程序
        self.init_program()

        # 主循环
        while True:
            if not self.windowOver:
                # 绘制倒计时
                self.process_limitTime()

            for event in pygame.event.get():
                # 主动退出
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if self.windowOver and event.key == pygame.K_SPACE:
                        self.set_window()
                        self.init_program()
                        self.windowOver = False
            
                # 程序没结束时
                if not self.windowOver:
                    if event.type == pygame.MOUSEBUTTONDOWN:      # 鼠标点击
                        # 获取鼠标点击位置
                        mouseY, mouseX = pygame.mouse.get_pos()
                        # 超出范围判断
                        if mouseY > self.screenWidth or mouseX > self.screenWidth:
                            continue
                        positionX, positionY = self.change_position(mouseX, mouseY)
                        if event.button == 1:   # 左键落子
                            if self.ScanPoint.clickCell(positionX, positionY):
                                self.windowOver = True
                                self.program_over_fail((positionX, positionY))
                                continue
                        elif event.button == 3:   # 右键标记
                            self.ScanPoint.markCell(positionX, positionY)
                    
                        # 绘制
                        self.excute_program()
                        if self.ScanPoint.isWin():
                            self.windowOver = True
                            self.program_over_win()

            # 刷新屏幕
            pygame.time.wait(10)
            pygame.display.flip()

    # 初始化程序(程序内初始化放这)
    def init_program(self):
        # 生成扫雷地图
        self.ScanPoint.genarateMap()
        # 绘制地图
        self.display_map()

    # 绘制空白地图
    def display_map(self):
        # 绘制地图
        self.screen.fill(self.backgroundColor)
        for i in range(1, self.ScanPoint.mapCellSize):
            pygame.draw.line(self.screen, self.lineColor, (0, i*self.cellsSize), (self.screenWidth, i*self.cellsSize), 2)
            pygame.draw.line(self.screen, self.lineColor, (i*self.cellsSize, 0), (i*self.cellsSize, self.screenWidth), 2)
        pygame.draw.line(self.screen, self.lineColor, (0, (i+1)*self.cellsSize), (self.screenWidth, (i+1)*self.cellsSize), 2)

    # 执行程序(程序内执行操作放这)
    def excute_program(self):
        # 先清空地图重新绘制
        self.display_map()
        # 绘制百分比
        precentLList = self.ScanPoint.displayMapList
        for i in range (0, len(precentLList)):
            precentlist = precentLList[i]
            for j in range (0, len(precentlist)):
                strChar = precentlist[j]
                if strChar == "#":
                    pass
                elif strChar == "@":
                    self.displayTxt("+", j*self.cellsSize, i*self.cellsSize)
                elif strChar == "0":
                    self.display_rect(j*self.cellsSize, i*self.cellsSize)
                else:
                    self.display_rect(j*self.cellsSize, i*self.cellsSize)
                    self.displayTxt(strChar, j*self.cellsSize, i*self.cellsSize)

    # 绘制文本
    def displayTxt(self, strNum, positionX, positionY, color=(255, 0, 0)):
        text = self.font.render(strNum, True, color)
        self.screen.blit(text, (positionX + self.fontHorizontalSize, positionY + self.fontVerticalSize))

    # 程序结束-失败
    def program_over_fail(self, clickPosition):
        # 绘制结束界面
        self.displayTxt("fail!", self.screenWidth/2-self.cellsSize, self.screenheight-self.cellsSize, self.RedColor)
        # 显示地雷位置
        for bombPosition in self.ScanPoint.bombPositionList:
            positionX = bombPosition[0] * self.cellsSize
            positionY = bombPosition[1] * self.cellsSize
            if clickPosition == bombPosition:
                self.displayTxt("*", positionY, positionX, self.clickBombColor)
            else:
                self.displayTxt("*", positionY, positionX, self.bombColor)

    # 程序结束-胜利
    def program_over_win(self):
        self.displayTxt("win!", self.screenWidth/2-self.cellsSize, self.screenheight-self.cellsSize, self.RedColor)

    # 转换坐标
    def change_position(self, mouseX, mouseY):
        positionX = int(mouseX / self.cellsSize)
        positionY = int(mouseY / self.cellsSize)
        return positionX, positionY

    # 绘制小格
    def display_rect(self, positionX, positionY):
        pygame.draw.rect(self.screen, self.LightGrayColor, (positionX+2, positionY+2, self.cellsSize-2, self.cellsSize-2))

    # 显示倒计时
    def process_limitTime(self):
        # 获取剩余时间
        strLimitTime = self.ScanPoint.getRemainTime()
        # 覆盖指定区域
        pygame.draw.rect(self.screen, self.backgroundColor, (0, self.screenWidth+2, self.screenWidth, self.cellsSize))
        self.displayTxt(strLimitTime, 0, self.screenheight-self.cellsSize, self.RedColor)
        # 时间是否结束判断
        if self.ScanPoint.isTimeOut():
            self.windowOver = True
            self.displayTxt("fail!", self.screenWidth/2-self.cellsSize, self.screenheight-self.cellsSize, self.RedColor)

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.start()
