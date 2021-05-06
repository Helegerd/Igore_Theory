# Coding:utf-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QFont
import sys
from random import shuffle, randint, choice
# для проверки
p1win = False
v1loose = False

def isTryNorm(buncharr=[5], winnum=66, actionarr=['*2', '+3'], winreq='неудП1;WВ1', lookexisting=True, currturn=1):
    '''ФУНКЦИЯ НЕ ИСПОЛЬЗУЕТСЯ И НЕ РАБОТАЕТ, оставил из-за жалости
    функция, которая проверяет, может ли куча(и) в bucharr удовлетворять условию в winreq -> True/False
    winnum -- количество балов, относительно которого считается победа
    actionarr -- перечень действий, который можно совершать с кучами
    lookexisting -- True если ещем, есть ли хотя бы одно удовлетворение условию, False если хотя бы одно несовпадение с условием
    currturn -- текущий ход (1-П1, 2-В1, 3-П2, 4-В2)'''
    if currturn > 4:  # перестраховка от слишком глубокой рекурсии
        return False
    # проверка сложных условий
    if winreq == 'неудП1;WВ1':  # неудачный П1, победный В1
        return isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ1', lookexisting=True, currturn=1) and\
               (isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WП1', lookexisting=True, currturn=1) or\
               isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ1', lookexisting=False, currturn=1))
    if winreq == '-WП1;WВ1':  # проигрышный П1, победный В1
        return isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ1', lookexisting=True, currturn=1)
    if winreq == '-WП1;-WВ1;WП2':  # проигрышный П1, проигрышный В1, победный П2
        return isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WП2', lookexisting=True, currturn=1)
    if winreq == 'WВ1негарант;WВ2':  # выигрышные В1 или В2, но В1 не гарантированно
        return isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ1', lookexisting=True, currturn=1) and\
               isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ1', lookexisting=False, currturn=1) and\
               isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ2', lookexisting=True, currturn=1)
    
    for i in range(len(buncharr)):
        for action in actionarr:
            helpbuncharr = buncharr[:]  # для манипуляций с кучами
            # увеличение кучки
            if action[0] == '+':  # плюсуем число
                helpbuncharr[i] += int(action[1:])
            elif action[0] == '*':  # умножаем на число
                helpbuncharr[i] *= int(action[1:])
            elif action == 'another':  # плюсуем другую кучку
                helpbuncharr[i] += helpbuncharr[1 - i]
                
            # проверка простых условий
            if winreq == 'WП1':  # выигрышный П1
                if (lookexisting and sum(helpbuncharr) >= winnum or not(lookexisting) and sum(helpbuncharr) < winnum) and currturn == 1:
                    return True
            if winreq == 'WВ1': # выигрышный В1
                if (lookexisting and sum(helpbuncharr) >= winnum or not(lookexisting) and sum(helpbuncharr) < winnum) and currturn == 2 or\
                   currturn < 2 and sum(helpbuncharr) < winnum and\
                   isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ1', lookexisting=lookexisting, currturn=currturn + 1):
                    return True
            if winreq == 'WП2': # выигрышный П2
                if (lookexisting and sum(helpbuncharr) >= winnum or not(lookexisting) and sum(helpbuncharr) < winnum) and currturn == 3 or\
                   currturn < 3 and sum(helpbuncharr) < winnum and\
                   isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WП2', lookexisting=lookexisting, currturn=currturn + 1):
                    return True
            if winreq == 'WВ2': # выигрышный В2
                if (lookexisting and sum(helpbuncharr) >= winnum or not(lookexisting) and sum(helpbuncharr) < winnum) and currturn == 4 or\
                   currturn < 4 and sum(helpbuncharr) < winnum and\
                   isTryNorm(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='WВ2', lookexisting=lookexisting, currturn=currturn + 1):
                    return True
    return False

def isAttemptOk(buncharr=[5], winnum=82, actionarr=['*2', '+3'], winreq='неудП1;WВ1', currturn=1):
    '''возвращает, подходит ли такая пара для данного условия
    buncharr -- массив с кучами
    winnum -- число, которому должна равняться сумма камней для победы
    actionarr -- массив с тем, что можно делать с кучами
    winreq -- условие для победы
    currturn -- текущий ход (1-П1, 2-В1, 3-П2, 4-В2)
    '''
    global p1win, v1loose
    allisok = False  # как ещё её назвать?
    
    if winreq == 'неудП1;WВ1':  # неудачный П1, победный В1
        p1win = False
        v1loose = False
        if currturn == 1:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum:  # если победный П1
                        p1win = True
                        continue
                    if isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=2):
                        allisok = True
            return allisok and (p1win or v1loose)
        elif currturn == 2:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) < winnum:  # если В1 проигрышный
                        v1loose = True
                    else:
                        allisok = True
            return allisok
    
    if winreq == '-WП1;WВ1':  # проигрышный П1, победный В1
        if currturn == 1:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum or not isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=2):
                        return False
            return True
        if currturn == 2:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum:
                        return True
            return False
        
    if winreq == '-WП1;-WВ1;WП2':  # проигрышный П1, проигрышный В1, победный П2
        if currturn == 1:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=2):
                        return True
            return False
        if currturn == 2:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum or not isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=3):
                        return False
            return True
        if currturn == 3:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum:
                        return True
            return False
    
    if winreq == 'WВ1негарант;WВ2':  # выигрышные В1 или В2, но В1 не гарантированно
        if currturn == 1:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum or isAttemptOk(buncharr=buncharr, winnum=winnum, actionarr=actionarr, winreq='-WП1;WВ1')\
                       or not isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=2):
                        return False
            return True  # чтобы не было гарантированно В1 победным
        if currturn == 2:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum or isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=3):
                        return True
            return False
        if currturn == 3:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum or not isAttemptOk(buncharr=helpbuncharr, winnum=winnum, actionarr=actionarr, winreq=winreq, currturn=4):
                        return False
            return True
        if currturn == 4:
            for i in range(len(buncharr)):
                for action in actionarr:
                    helpbuncharr = buncharr[:]  # для манипуляций с кучами
                    # увеличение кучки
                    helpbuncharr = getArrForAct(helpbuncharr, action, i)
                    if sum(helpbuncharr) >= winnum:
                        return True
            return False
    

def getArrForAct(arr, action, ind):
    '''возвращает список, сотворённый по указанному действию act с ind-овым числом arr'''
    if action[0] == '+':  # плюсуем число
        arr[ind] += int(action[1:])
    elif action[0] == '*':  # умножаем на число
        arr[ind] *= int(action[1:])
    elif action == 'another':  # плюсуем другую кучку
        if ind == 0:
            arr[0] += arr[1]
        elif ind == 1:
            arr[1] += arr[0]
    return arr

def getAnsFormatText(form='min'):
    '''возвращает тект для вопроса о формате вывода'''
    # ['min', 'max', 'minmax', 'anytwo', 'anyone', 'num']
    return {'min': 'Укажите, при каком минимальном значении S это возможно.',
            'max': 'Укажите, при каком максимальном значении S это возможно.',
            'minmax': 'Укажите в порядке возрастания, при каких наименьшем и наибольшем значениях S это возможно.',
            'anytwo': 'Укажите 2 любых значения S, при которых данное условие выполняется.',
            'anyone': 'Укажите любое значение S, при котором данное условие выполняется.',
            'num': 'Укажите количество значений S, при которых данное условие выполняется.'}[form]

def getAnsText(ans='неудП1;WВ1'):
    '''Возвращает условие вопроса'''
    return {'неудП1;WВ1': 'Ваня выигрывает своим первым ходом после неудачного первого хода Пети.',
            '-WП1;WВ1': 'Ваня выигрывает своим первым ходом при любой игре Пети.',
            '-WП1;-WВ1;WП2': 'Петя не может выиграть своим первым ходом, но выигрывает своим вторым ходом при любой игре Вани.',
            'WВ1негарант;WВ2': 'Ваня выигрывает первым или вторым ходом, но не гарантировано, что первым.'}[ans]

def getPosQuest(answersnum=0):
    '''возвращает вопрос, корректный к данному количеству ответов answersnum'''
    retarr = ['num']
    if answersnum > 0:
        retarr = retarr + ['min', 'max', 'anyone', 'minmax']
    if answersnum > 1:
        retarr = retarr + ['anytwo']
    return choice(retarr)



class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.dist = 5  # расстояние между полями в пикселях
        self.formarr = []  # массив, где говорится, где в каком формате должен бвть ответ
        
        # поля условия и вопросов
        self.fields = []
        for i in range(4):
            self.fields.append(QTextBrowser(self))
            self.fields[-1].resize(600, 150)
            self.fields[-1].move(50, i * (self.fields[-1].height() + self.dist) + self.dist)
            self.fields[-1].setFont(QFont('Ariel', 10))
        self.fields[0].resize(700, self.fields[0].height())
        self.fields[0].move(50, self.dist)
            
        # эдиты для ответов
        self.ansarr = [QLineEdit(self) for _i in range(3)]
        for i in range(len(self.ansarr)):
            self.ansarr[i].resize(100, 50)
            self.ansarr[i].move(self.fields[i + 1].x() + self.fields[i + 1].width() + self.dist, (1 + i) * (self.fields[-1].height() + self.dist) + self.dist)
        # кнопка проверки ответов
        self.checkbtn = QPushButton(self)
        self.checkbtn.resize(200, 50)
        self.checkbtn.setFont(QFont('Arial', 15))
        self.checkbtn.setText('ПРОВЕРИТЬ')
        self.checkbtn.move(550, 700)
        self.checkbtn.clicked.connect(self.check)
        
        # кнопка для обновления задачи
        self.refreshbtn = QPushButton(self)
        self.refreshbtn.resize(150, 50)
        self.refreshbtn.move(50, 700)
        self.refreshbtn.setFont(QFont('Arial', 15))
        self.refreshbtn.setText('ОБНОВИТЬ')
        self.refreshbtn.clicked.connect(self.refresh)
        
        # лабелы для проверки
        self.anslabs = [QLabel(self) for _i in range(3)]
        for i in range(len(self.anslabs)):
            self.anslabs[i].resize(100, 50)
            self.anslabs[i].move(self.fields[i + 1].x() + self.fields[i + 1].width() + self.dist, self.ansarr[i].y() + self.ansarr[i].height() + self.dist)
        
    def refresh(self):
        '''данные и виджеты обновляются'''
        for lab in self.anslabs:  # прячем лабелы с ответами
            lab.hide()
        for edit in self.ansarr:  # чистим эдиты
            edit.setText('')
        self.bunchnum = randint(1, 2)  # количество кучек
        self.winnum = randint(51, 101)  # сколько должно быть для победы
        self.actionarr = []  # то, какие действия можно свершать над кучами
        if self.bunchnum == 2:
            self.actionarr.append('another')
        self.actionarr = self.actionarr + ['+' + str(i) for i in range(1, 5)] + ['*' + str(i) for i in range(2, 4)]
        shuffle(self.actionarr)
        self.actionarr = self.actionarr[:randint(2, 4)]
        self.bunches = []
        if self.bunchnum == 2:
            self.bunches = [randint(0, 5), 0]
        else:
            self.bunches = [0]
        self.formarr = []  # для форматов ответа
        self.questions = [choice(['-WП1;WВ1', 'неудП1;WВ1']), '-WП1;-WВ1;WП2', 'WВ1негарант;WВ2']  # условия для вопросов
        self.answers = [[] for _i in range(3)]  # массивы с ответами на вопросы
        s = ''  # просто вспомогательная строка
        
        # заполнение первого браузера (с условием)
        s = 'Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками '
        if self.bunchnum == 1:
            s = s + 'лежит одна куча камней. '
        elif self.bunchnum == 2:
            s = s + 'лежат две кучи камней. '
        s = s + 'Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может с одной из имеющихся куч выполнить следующие действия: '
        for act in self.actionarr:
            if act[0] == '+':
                s = s + 'добавить ' + act[1:] + ', '
            elif act[0] == '*':
                s = s + 'умножить на ' + act[1:] + ', '
            elif act == 'another':
                s = s + 'добавить столько же, сколько сейчас в другой куче, '
        s = s[:-2] + '. '
        s = s + 'Игра завершается в тот момент, когда суммарное количество камней в кучах становится не менее ' + str(self.winnum) + '. '
        s = s + 'Победителем считается игрок, сделавший последний ход. '
        if self.bunchnum == 1:
            s = s + 'В начальный момент в единственной куче количество камней было равно S, 1 <= S < ' + str(self.winnum) + '. '
        elif self.bunchnum == 2 and self.bunches[0] == 0:  # 2 переменные
            s = s + f'В начальный момент в первой куче количество камней было равно S, во второй -- K, 1 <= S < {self.winnum}, 1 <= K < {self.winnum}. '
        elif self.bunchnum == 2:
            s = s + f'В начальный момент в первой куче количество камней было равно {self.bunches[0]}, во второй -- S, 1 <= S < {self.winnum}. '
        self.fields[0].setText(s)
        
        # делаем варианты ответов к первому вопросу
        k = 0  # для случаев, когда 2 переменные
        if self.bunchnum == 2 and self.bunches[0] == 0:
            k = randint(1, 12)
        for num in range(1, self.winnum):
            if self.bunchnum == 1 and isAttemptOk(buncharr=[num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[0]) or\
               self.bunchnum == 2 and self.bunches[0] == 0 and isAttemptOk(buncharr=[k, num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[0]) or\
               self.bunchnum == 2 and self.bunches[0] != 0  and isAttemptOk(buncharr=[self.bunches[0], num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[0]):
                self.answers[0].append(num)
        self.formarr.append(getPosQuest(len(self.answers[0])))
        
        # заполняем первый вопрос
        s = getAnsText(self.questions[0]) + ' '
        if self.bunchnum == 2 and self.bunches[0] == 0:
            s = s + f'K = {k}. '
        s = s + getAnsFormatText(self.formarr[0])
        self.fields[1].setText(s)
        
        # делаем варианты ответов ко второму вопросу
        k = 0  # для случаев, когда 2 переменные
        if self.bunchnum == 2 and self.bunches[0] == 0:
            k = randint(1, 12)
        for num in range(1, self.winnum):
            if self.bunchnum == 1 and isAttemptOk(buncharr=[num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[1]) or\
                   self.bunchnum == 2 and self.bunches[0] == 0 and isAttemptOk(buncharr=[k, num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[1]) or\
                   self.bunchnum == 2 and self.bunches[0] != 0  and isAttemptOk(buncharr=[self.bunches[0], num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[1]):
                self.answers[1].append(num)
        self.formarr.append(getPosQuest(len(self.answers[1])))
        
        # заполняем второй вопрос
        s = getAnsText(self.questions[1]) + ' '
        if self.bunchnum == 2 and self.bunches[0] == 0:
            s = s + f'K = {k}. '
        s = s + getAnsFormatText(self.formarr[1])
        self.fields[2].setText(s)
        
        # делаем варианты ответов к третьему вопросу
        k = 0  # для случаев, когда 2 переменные
        if self.bunchnum == 2 and self.bunches[0] == 0:
            k = randint(1, 12)
        for num in range(1, self.winnum):
            if self.bunchnum == 1 and isAttemptOk(buncharr=[num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[2]) or\
                   self.bunchnum == 2 and self.bunches[0] == 0 and isAttemptOk(buncharr=[k, num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[2]) or\
                       self.bunchnum == 2 and self.bunches[0] != 0  and isAttemptOk(buncharr=[self.bunches[0], num], winnum=self.winnum, actionarr=self.actionarr, winreq=self.questions[2]):
                self.answers[2].append(num)
        self.formarr.append(getPosQuest(len(self.answers[2])))  # выбираем рандомный формат ответ (минимальный, любой, 2 любых и т.д.)
        
        # заполняем третий вопрос
        s = getAnsText(self.questions[2]) + ' '
        if self.bunchnum == 2 and self.bunches[0] == 0:
            s = s + f'K = {k}. '
        s = s + getAnsFormatText(self.formarr[2])
        self.fields[3].setText(s)
        
        for ans in self.answers:
            print(len(ans), ans)
        
    def check(self):
        '''проверка введённых ответов'''
        for i in range(3):
            # ['num', 'min', 'max', 'anyone', 'minmax', 'anytwo']
            try:
                answer = list(map(int, self.ansarr[i].text().split()))
                if self.formarr[i] == 'num' and answer[0] == len(self.answers[i]) or self.formarr[i] == 'min' and answer[0] == min(self.answers[i]) or\
                   self.formarr[i] == 'max' and answer[0] == max(self.answers[i]) or self.formarr[i] == 'anyone' and answer[0] in self.answers[i] or\
                   self.formarr[i] == 'minmax' and answer[0] == min(self.answers[i]) and answer[1] == max(self.answers[i]) or\
                   self.formarr[i] == 'anytwo' and answer[0] in self.answers[i] and answer[1] in self.answers[i]:
                    self.anslabs[i].setText('<p style="color: rgb(50, 200, 50);">Да!</p>')
                else:
                    self.anslabs[i].setText('<p style="color: rgb(250, 50, 50);">Нет</p>')
            except:
                self.anslabs[i].setText('<p style="color: rgb(250, 50, 50);">Повторите ввод</p>')
        for lab in self.anslabs:
            lab.show()
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MW()
    mw.show()
    sys.exit(app.exec_())