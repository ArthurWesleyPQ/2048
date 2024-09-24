from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from functools import partial
from random import randint

KV = '''
<HomeScreen>:
    orientation: 'vertical'
    FloatLayout:
        FloatLayout:
            id: game_lyt
            size_hint: 1, None
            height: self.width
            pos: self.parent.pos
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        FloatLayout:
            size_hint: 1, 1
            pos: 0, root.ids.btns_lyt.height + root.ids.game_lyt.height
            canvas.before:
                Color:
                    rgba: 0,0,0,1
                Rectangle:
                    pos: self.pos
                    size: self.size
        FloatLayout:
            size_hint: 1, 1
            canvas.before:
                Color:
                    rgba: 0,0,0,1
                Rectangle:
                    pos: self.pos
                    size: self.size
    FloatLayout:
        id: btns_lyt
        GameButtons:
            size_hint: 1/2, None
            pos: self.width / 2, self.parent.height - self.height * 1.25
        ScoreLabel:
            id: score_label
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}

<DirectionalButton>:
    on_press: root.onBtnPress()
    Image:
        source: 'arr.png'
        size: self.parent.size
        pos: self.parent.pos
        canvas.before:
            PushMatrix
            Rotate:
                origin: self.center
                angle: 90 if root.btn_dir == "left" else 180 if root.btn_dir == "down" else 270 if root.btn_dir == "right" else 0
        canvas.after:
            PopMatrix
            
<GameButtons>:
    cols: 3
    rows: 3
    height: self.width
    Label:
    DirectionalButton:
        btn_dir: "up"
    Label:
    DirectionalButton:
        btn_dir: "left"
    Label:
    DirectionalButton:
        btn_dir: "right"
    Label:
    DirectionalButton:
        btn_dir: "down"
    Label:
        
<ScoreLabel>:
    text: "Score: {0}".format(root.score)
    font_size: '40dp'
    markup: True
    
<NumberBlock>:
    size_hint: 1/4, None
    pos: self.pos
    height: self.width
    green: (0.2352, 0.7, 0.4432, 1)
    blue: (0.3921, 0.5843, 0.9294, 1)
    yellow: (0.9921, 0.8549, 0.0509, 1)
    red: (0.8235, 0.1686, 0.1686, 1)
    byzantium: (0.4392, 0.1607, 0.3882, 1)
    orchid: (0.8549, 0.4392, 0.8392, 1)
    light_gray: (0.8274, 0.8274, 0.8274, 1)
    terracota: (0.8862, 0.4470, 0.3568, 1)
    mud: (0.4392, 0.3294, 0.2431, 1)
    turquoise: (0.2509, 0.8784, 0.8156, 1)
    adamantium: (0.3529, 0.2901, 0.3294, 1)
    canvas.before:
        Color:
            rgba: self.green if root.value == '2' else self.blue if root.value == '4' else self.yellow if root.value == '8' else self.red if root.value == "16" else self.byzantium if root.value == "32" else self.orchid if root.value == "64" else self.light_gray if root.value == "128" else self.terracota if root.value == "256" else self.mud if root.value == "512" else self.turquoise if root.value == "1024" else self.adamantium
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        text: root.value
'''

Builder.load_string(KV)

CLOCK_INTERVAL = 1/60
CLOCK_ANIMATION_MULTIPLIER = 1
NB_ANIMATION_SPEED = 3000

MIN_STARTING_BLOCKS_QNT = 4
MAX_STARTING_BLOCKS_QNT = 8

class NumberBlock(BoxLayout):
    value = StringProperty()
    animating = False
    merge = False
    selfLineCol = (0, 0)
    
    def animate(self, dir, pos, line_col, adjust=False, *args):
        app = App.get_running_app()
        if dir == "down":
            if adjust == True:
                self.pos = self.width * self.selfLineCol[1], self.parent.pos[1] + self.parent.height
                self.opacity = 1
                self.disable = False
            self.event = Clock.schedule_interval(partial(self.descend_pos, pos, line_col, app), CLOCK_INTERVAL)
        elif dir == "up":
            if adjust == True:
                self.pos = self.width * self.selfLineCol[1], self.parent.pos[1] + self.parent.height - self.height - (self.height * 4)
                self.opacity = 1
                self.disable = False
            self.event = Clock.schedule_interval(partial(self.ascend_pos, pos, line_col, app), CLOCK_INTERVAL)
        elif dir == "left":
            if adjust == True:
                self.pos = self.parent.width, self.parent.pos[1] + self.parent.height - self.height - (self.height * self.selfLineCol[0])
                self.opacity = 1
                self.disable = False
            self.event = Clock.schedule_interval(partial(self.left_pos, pos, line_col, app), CLOCK_INTERVAL)
        elif dir == "right":
            if adjust == True:
                self.pos = self.parent.width - self.width - (self.width * 4), self.parent.pos[1] + self.parent.height - self.height - (self.height * self.selfLineCol[0])
                self.opacity = 1
                self.disable = False
            self.event = Clock.schedule_interval(partial(self.right_pos, pos, line_col, app), CLOCK_INTERVAL)
       
    def descend_pos(self, pos, line_col, app, *args):
        newPos = self.pos[0], self.pos[1] - CLOCK_INTERVAL * CLOCK_ANIMATION_MULTIPLIER * NB_ANIMATION_SPEED
        if newPos[1] <= self.parent.pos[1] + self.height * pos:
            newPos = self.pos[0], self.parent.pos[1] + self.height * pos
            
            self.animating = False
            Clock.unschedule(self.event)
            if self.merge:
                self.do_merge(line_col, app)
        self.pos = newPos
        
    def ascend_pos(self, pos, line_col, app, *args):
        newPos = self.pos[0], self.pos[1] + CLOCK_INTERVAL * CLOCK_ANIMATION_MULTIPLIER * NB_ANIMATION_SPEED
        if newPos[1] >= self.parent.pos[1] + self.parent.height - self.height - (self.height * pos):
            newPos = self.pos[0], self.parent.pos[1] + self.parent.height - self.height - (self.height * pos)
            
            self.animating = False
            Clock.unschedule(self.event)
            if self.merge:
                self.do_merge(line_col, app)
        self.pos = newPos
    
    def left_pos(self, pos, line_col, app, *args):
        newPos = self.pos[0] - CLOCK_INTERVAL * CLOCK_ANIMATION_MULTIPLIER * NB_ANIMATION_SPEED, self.pos[1]
        if newPos[0] <= self.width * pos:
            newPos = self.width * pos, self.pos[1]
            
            self.animating = False
            Clock.unschedule(self.event)
            if self.merge:
                self.do_merge(line_col, app)
        self.pos = newPos
        
    def right_pos(self, pos, line_col, app, *args):
        newPos = self.pos[0] + CLOCK_INTERVAL * CLOCK_ANIMATION_MULTIPLIER * NB_ANIMATION_SPEED, self.pos[1]
        if newPos[0] >= self.parent.width - self.width - (self.width * pos):
            newPos = self.parent.width - self.width - (self.width * pos), self.pos[1]
            self.animating = False
            Clock.unschedule(self.event)
            if self.merge:
                self.do_merge(line_col, app)
        self.pos = newPos
        
    def do_merge(self, line_col, app):
        try:
            app.gameArray[line_col[0]][line_col[1]].value = str(int(self.value) * 2)
            app.hs.ids.score_label.score = str(int(app.hs.ids.score_label.score) + int(self.value) * 2)
        except:
            pass
        self.parent.remove_widget(self)

class ScoreLabel(Label):
    score = StringProperty('0')

class GameButtons(GridLayout):
    pass

class DirectionalButton(Button):
    btn_dir = StringProperty()
    
    def onBtnPress(self):
        app = App.get_running_app()
        animating = False
        line_col = (0, 0)
        newGameArray = [[None, None, None, None],
                                        [None, None, None, None],
                                        [None, None, None, None],
                                        [None, None, None, None]]
        gameArray = app.gameArray
        
        for line in range(4):
            if not animating:
                for column in range(4):
                    curNB = gameArray[line][column]
                
                    if curNB != None and curNB.animating:
                        animating = True
                        break
            else:
                break
        
        if not animating:
            if self.btn_dir == "right":
                for line in range(4):
                    lineCount = 0
                    lineVals = []
                    animCount = 0
                    
                    for column in range(3, -1, -1):
                        curNB = gameArray[line][column]
                        
                        if curNB != None:
                            curNB.animating = True
                            count = 0
                            lookForSameValue = True
                            
                            for x in range(column + 1, 4, 1):
                                curCmpNB = gameArray[line][x]
                                
                                if curCmpNB != None:
                                    if not curCmpNB.merge:
                                        if lookForSameValue:
                                            lookForSameValue = False
                                            if curNB.value == curCmpNB.value:
                                                curNB.merge = True
                                                line_col = curCmpNB.selfLineCol
                                                animCount += 1
                                            else:
                                                count += 1 
                                        else:
                                            count += 1
                                    else:
                                        lookForSameValue = False
                                else:
                                    animCount += 1
                            
                            if not curNB.merge:
                                curNB.selfLineCol = (line, 3 - count)
                                newGameArray[line][3 - count] = curNB
                                lineCount += 1
                                lineVals.append(curNB.value)
                                
                            Clock.schedule_once(partial(curNB.animate, self.btn_dir, count, line_col))
                    else:
                        # spawn NumberBlock
                        if lineCount < 4 and animCount > 0:
                            randChance = randint(0, 99)
                            
                            if randChance <= 19:
                                game = app.hs.ids.game_lyt
                                
                                selVal = lineVals[randint(0, len(lineVals) - 1)]
                                
                                nb = NumberBlock(value=selVal)
                                
                                newGameArray[line][3 - lineCount] = nb
                                nb.selfLineCol = line, 3 - lineCount
                                
                                nb.animating = True
                                nb.opacity = 0
                                nb.disable = True
                                game.add_widget(nb)
                                
                                Clock.schedule_once(partial(nb.animate, self.btn_dir, lineCount, None, True))
                            
            elif self.btn_dir == "left":
                for line in range(4):
                    lineCount = 0
                    lineVals = []
                    animCount = 0
                    
                    for column in range(4):
                        curNB = gameArray[line][column]
                        
                        if curNB != None:
                            curNB.animating = True
                            count = 0
                            lookForSameValue = True
                            
                            for x in range(column -1, -1, -1):
                                curCmpNB = gameArray[line][x]
                                
                                if curCmpNB != None:
                                    if not curCmpNB.merge:
                                        if lookForSameValue:
                                            lookForSameValue = False
                                            if curNB.value == curCmpNB.value:
                                                curNB.merge = True
                                                line_col = curCmpNB.selfLineCol
                                                animCount += 1
                                            else:
                                                count += 1
                                        else:
                                            count += 1
                                    else:
                                        lookForSameValue = False
                                else:
                                    animCount += 1
                            
                            if not curNB.merge:
                                curNB.selfLineCol = (line, count)
                                newGameArray[line][count] = curNB
                                lineCount += 1
                                lineVals.append(curNB.value)
                                
                            Clock.schedule_once(partial(curNB.animate, self.btn_dir, count, line_col))
                    else:
                        # spawn NumberBlock
                        if lineCount < 4 and animCount > 0:
                            randChance = randint(0, 99)
                            
                            if randChance <= 19:
                                game = app.hs.ids.game_lyt
                                
                                selVal = lineVals[randint(0, len(lineVals) - 1)]
                                
                                nb = NumberBlock(value=selVal)
                                
                                newGameArray[line][lineCount] = nb
                                nb.selfLineCol = line, lineCount
                                
                                nb.animating = True
                                nb.opacity = 0
                                nb.disable = True
                                game.add_widget(nb)
                                
                                Clock.schedule_once(partial(nb.animate, self.btn_dir, lineCount, None, True))
                
            elif self.btn_dir == "up":
                for column in range(4):
                    colCount = 0
                    colVals = []
                    animCount = 0
                    
                    for line in range(4):
                        curNB = gameArray[line][column]
                        
                        if curNB != None:
                            curNB.animating = True
                            count = 0
                            lookForSameValue = True
                            
                            for x in range(line - 1, -1, -1):
                                curCmpNB = gameArray[x][column]
                                
                                if curCmpNB != None:
                                    if not curCmpNB.merge:
                                        if lookForSameValue:
                                            lookForSameValue = False
                                            if curNB.value == curCmpNB.value:
                                                curNB.merge = True
                                                line_col = curCmpNB.selfLineCol
                                                animCount += 1
                                            else:
                                                count += 1
                                        else:
                                            count += 1
                                    else:
                                        lookForSameValue = False
                                else:
                                    animCount += 1
                            
                            if not curNB.merge:
                                curNB.selfLineCol = (count, column)
                                newGameArray[count][column] = curNB
                                colCount += 1
                                colVals.append(curNB.value)
                                
                            Clock.schedule_once(partial(curNB.animate, self.btn_dir, count, line_col))
                    else:
                        # spawn NumberBlock
                        if colCount < 4 and animCount > 0:
                            randChance = randint(0, 99)
                            
                            if randChance <= 19:
                                game = app.hs.ids.game_lyt
                                
                                selVal = colVals[randint(0, len(colVals) - 1)]
                                
                                nb = NumberBlock(value=selVal)
                                
                                newGameArray[colCount][column] = nb
                                nb.selfLineCol = colCount, column
                                
                                nb.animating = True
                                nb.opacity = 0
                                nb.disable = True
                                game.add_widget(nb)
                                
                                Clock.schedule_once(partial(nb.animate, self.btn_dir, colCount, None, True))
                
            elif self.btn_dir == "down":
                for column in range(4):
                    colCount = 0
                    colVals = []
                    animCount = 0
                    
                    for line in range(3, -1, -1):
                        curNB = gameArray[line][column]
                        
                        if curNB != None:
                            curNB.animating = True
                            count = 0
                            lookForSameValue = True
                            
                            for x in range(line + 1, 4, 1):
                                curCmpNB = gameArray[x][column]
                                
                                if curCmpNB != None:
                                    if not curCmpNB.merge:
                                        if lookForSameValue:
                                            lookForSameValue = False
                                            if curNB.value == curCmpNB.value:
                                                curNB.merge = True
                                                line_col = curCmpNB.selfLineCol
                                                animCount += 1
                                            else:
                                                count += 1
                                        else:
                                            count += 1
                                    else:
                                        lookForSameValue = False
                                else:
                                    animCount += 1
                            
                            if not curNB.merge:
                                curNB.selfLineCol = (3 - count, column)
                                newGameArray[3 - count][column] = curNB
                                colCount += 1
                                colVals.append(curNB.value)
                                
                            Clock.schedule_once(partial(curNB.animate, self.btn_dir, count, line_col))
                    else:
                        # spawn NumberBlock
                        if colCount < 4 and animCount > 0:
                            randChance = randint(0, 99)
                            
                            if randChance <= 19:
                                game = app.hs.ids.game_lyt
                                
                                selVal = colVals[randint(0, len(colVals) - 1)]
                                
                                nb = NumberBlock(value=selVal)
                                
                                newGameArray[3 - colCount][column] = nb
                                nb.selfLineCol = 3 - colCount, column
                                
                                nb.animating = True
                                nb.opacity = 0
                                nb.disable = True
                                game.add_widget(nb)
                                
                                Clock.schedule_once(partial(nb.animate, self.btn_dir, colCount, None, True))
                
            app.gameArray = newGameArray

class HomeScreen(BoxLayout):
    
    def setupGameWidgets(self, gameArray, *args):
        game = self.ids.game_lyt
        
        for line in range(4):
            for column in range(4):
                curNB = gameArray[line][column]
                
                if curNB != None:
                    curNB.opacity = 0
                    curNB.disable = True
                    game.add_widget(curNB)
                else:
                    Clock.schedule_once(partial(self.adjustGameWidgets, gameArray))
   
    def adjustGameWidgets(self, gameArray, *args):
        game = self.ids.game_lyt
        
        for line in range(4):
            for column in range(4):
                curNB = gameArray[line][column]
               
                if curNB != None:
                    curNB.pos = game.pos[0] + curNB.width * column, game.pos[1] +  game.height - curNB.height - (curNB.height * line)
                    curNB.opacity = 1
                    curNB.disable = False

class MyApp(App):
    gameArray = [[None, None, None, None],
                             [None, None, None, None],
                             [None, None, None, None],
                             [None, None, None, None]]
    hs = HomeScreen()
    
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        Clock.schedule_once(self.setupGame)
        
    def setupGame(self, *args):         
           qnt = randint(MIN_STARTING_BLOCKS_QNT, MAX_STARTING_BLOCKS_QNT)
           
           for x in range(qnt):
               rand_line = randint(0, 3)
               rand_column = self.generate_rand_column(rand_line)
               
               while self.gameArray[rand_line][rand_column] != None:
                   rand_line = randint(0, 3)
                   rand_column = self.generate_rand_column(rand_line)
               else:
                   rand_val = randint(0,2)
                   val = '0'
                   if rand_val == 0:
                       val = '2'
                   elif rand_val == 1:
                       val = '4'
                   else:
                       val = '8'
                       
                   self.gameArray[rand_line][rand_column] = NumberBlock(value=val)
           
           else:
               Clock.schedule_once(partial(self.hs.setupGameWidgets, self.gameArray))
           
    def generate_rand_column(self, rand_line):
        ret = randint(0, 3)
        if rand_line == 0 or rand_line == 3:
            return ret
        else:
            val = randint(0, 1)
            if val == 0:
                return 0
            else:
                return 3
           
    def build(self):
        return self.hs
        
if __name__ == '__main__':
    MyApp().run()
