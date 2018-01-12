from Tkinter import *
from operator import itemgetter, attrgetter, methodcaller
import urllib
import urllib2
import json
import math

class Application(Frame):

    _host = 'http://api.h.miguan.in'
    _app = _host + '/game'
    _homePage = _app + '/homePage'
    _filterHomePage = _app + '/filterHomePage'

    _pageSize = 21
    _generationFactor = 0.168
    _bearFactor = 0.42
    _birthMin = 30

    _page = 0

    _httpClient = None

    _accessToken = ''
    _cookieStr = ''
    _monkeyList = []

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def searchIt(self, postMap, headerData, gen):
        self._genFactor = 1;
        if gen > -1:
            self._genFactor = math.pow(1+self._generationFactor, gen)
            postMap['startGen'] = gen
            postMap['endGen'] = gen
        print postMap
        try:
            _httpClient = urllib2.Request(url=self._filterHomePage,
                                           data=urllib.urlencode(postMap),
                                           headers=headerData)
            res_data = urllib2.urlopen(_httpClient)
            res = res_data.read()
            return json.loads(res)
        except Exception, e:
            print e

    def postRequest(self, next):
        self._addParam(next)
        #del self._monkeyList[:]
        for current in range( (self._page-1)*self._step+1, self._page*self._step+1 ):
            self._postMap['current'] = current
            resJson = self.searchIt(self._postMap, self._headerData, self._gen)
            if (resJson['code'] == 200):
                for monkey in resJson['result']['records']:
                    id = monkey['id']
                    generation = monkey['generation']
                    bearNum = monkey['bearNum']
                    bear = monkey['bear']
                    grow = monkey['grow']
                    makeMoney = monkey['makeMoney']
                    weight = monkey['weight']
                    price = monkey['price']

                    if self._gen == -1:
                        #self._gen = generation;
                        self._genFactor = math.pow(1 + self._generationFactor, generation)

                    threeD = round(bear + grow + makeMoney, 2)
                    bgm = round((threeD+weight/40)/(price), 2)
                    dig = round(weight*makeMoney/self._genFactor, 2)
                    birth = self._birthMin

                    monkeyMap = {}
                    monkeyMap['id'] = id
                    monkeyMap['dig'] = dig
                    monkeyMap['bgm'] = bgm
                    monkeyMap['bear'] = bear
                    monkeyMap['birth'] = birth
                    monkeyMap['grow'] = grow
                    monkeyMap['threeD'] = threeD
                    monkeyMap['makeMoney'] = makeMoney
                    monkeyMap['weight'] = round(weight, 2)
                    monkeyMap['generation'] = generation
                    monkeyMap['price'] = price
                    if threeD > 5:
                        self._monkeyList.append(monkeyMap)

        if self._sort == 0:
            newMonkeyList = sorted(self._monkeyList, key=lambda x:x['bgm'], reverse=False)
        else:
            newMonkeyList = sorted(self._monkeyList, key=lambda x: x['bgm'], reverse=True)

        idx = 0
        for monkey in newMonkeyList:
            #print monkey
            monkey['idx'] = idx
            idx+=1
            self.RESULTLIST.insert(END, monkey)


    def _addParam(self, next):
        self._accessToken = str(self.TOKENINPUT.get())
        self._cookieStr = "_ga=GA1.2.2065627706.1514962145; _gid=GA1.2.1066794520.1514962145; acw_tc=AQAAAIQtRl26KAYAchqntLHthZ87Cu58; token=" + self._accessToken
        #self.TOKENINPUT.delete(0, END)
        self.RESULTLIST.delete(0, END)

        self._headerData = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "accessToken": self._accessToken,
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": self._cookieStr,
            "Host": "api.h.miguan.in",
            "Origin": "http://h.miguan.in",
            "Referer": "http://h.miguan.in/market",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        if next != 0:
            self._page += next
            if self._page <= 0:
                self._page = 1
        else:
            self._page = int(self.PAGEINPUT.get())
            if self._page <= 0:
                self._page = 1
        self.PAGEINPUT.delete(0, END)
        self.PAGEINPUT.insert(END, self._page)

        self._step = int(self.STEPINPUT.get())
        self._gen = int(self.GENINPUT.get())
        self._orderBy = int(self.ORDERBYINPUT.get())
        self._sort = int(self.SORTINPUT.get())

        self._postMap = {'orderBy': self._orderBy,
                         'sort': 0,
                         'status': 1,
                         'id': '',
                         'gen': '',
                         'startGen': '',
                         'endGen': '',
                         'startGrow': '',
                         'endGrow': '',
                         'startBear': '',
                         'endBear': '',
                         'startMakeMoney': '',
                         'endMakeMoney': '',
                         'startBearNum': '',
                         'endBearNum': '',
                         'startWeight': '',
                         'endWeight': ''}

    def reset(self):
        self.PAGEINPUT.delete(0, END)
        self.PAGEINPUT.insert(END, 1)

        self.STEPINPUT.delete(0, END)
        self.STEPINPUT.insert(END, 5)

        self.GENINPUT.delete(0, END)
        self.GENINPUT.insert(END, -1)

        self.ORDERBYINPUT.delete(0, END)
        self.ORDERBYINPUT.insert(END, 1)

        self.SORTINPUT.delete(0, END)
        self.SORTINPUT.insert(END, 1)

        del self._monkeyList[:]
        self.postRequest(0)

    def createWidgets(self):

        self.PARAMFRAME = Frame(root)
        self.PARAMFRAME.pack(side=TOP)

        self.TOKENLABEL = Label(self.PARAMFRAME, text="accessToken")
        self.TOKENLABEL.pack(side=LEFT)
        self.TOKENINPUT = Entry(self.PARAMFRAME, width=100)
        self.TOKENINPUT.pack(side=LEFT)
        self.TOKENINPUT.delete(0, END)

        self.PARAMFRAME = Frame(root)
        self.PARAMFRAME.pack(side=TOP)

        self.PAGELABEL = Label(self.PARAMFRAME, text="page:")
        self.PAGELABEL.pack(side=LEFT)
        self.PAGEINPUT = Entry(self.PARAMFRAME, width=10)
        self.PAGEINPUT.pack(side=LEFT)
        self.PAGEINPUT.insert(0, "1")

        self.STEPLABEL = Label(self.PARAMFRAME, text="step:")
        self.STEPLABEL.pack(side=LEFT)
        self.STEPINPUT = Entry(self.PARAMFRAME, width=10)
        self.STEPINPUT.pack(side=LEFT)
        self.STEPINPUT.insert(0, "5")

        self.GENLABEL = Label(self.PARAMFRAME, text="gen:")
        self.GENLABEL.pack(side=LEFT)
        self.GENINPUT = Entry(self.PARAMFRAME, width=10)
        self.GENINPUT.pack(side=LEFT)
        self.GENINPUT.insert(0, "-1")

        self.ORDERBYLABEL = Label(self.PARAMFRAME, text="orderBy:")
        self.ORDERBYLABEL.pack(side=LEFT)
        self.ORDERBYINPUT = Entry(self.PARAMFRAME, width=10)
        self.ORDERBYINPUT.pack(side=LEFT)
        self.ORDERBYINPUT.insert(0, "1")

        self.SORTLABEL = Label(self.PARAMFRAME, text="sort:")
        self.SORTLABEL.pack(side=LEFT)
        self.SORTINPUT = Entry(self.PARAMFRAME, width=10)
        self.SORTINPUT.pack(side=LEFT)
        self.SORTINPUT.insert(0, "1")

        self.PARAMFRAME = Frame(root)
        self.PARAMFRAME.pack(side=TOP)

        self.CURRBUTTON = Button(self.PARAMFRAME, text="CURR", fg="red", command=lambda:self.postRequest(0))
        self.CURRBUTTON.pack(side=LEFT)

        # self.NEXTBUTTON = Button(self.PARAMFRAME, text="PREV", fg="red", command=lambda: self.postRequest(-1))
        # self.NEXTBUTTON.pack(side=LEFT)

        self.NEXTBUTTON = Button(self.PARAMFRAME, text="NEXT", fg="red", command=lambda: self.postRequest(1))
        self.NEXTBUTTON.pack(side=LEFT)

        self.RESETBUTTON = Button(self.PARAMFRAME, text="RESET", fg="red", command=self.reset)
        self.RESETBUTTON.pack(side=LEFT)

        self.QUITBUTTON = Button(self.PARAMFRAME, text="QUIT", fg="red", command=self.quit)
        self.QUITBUTTON.pack(side=RIGHT)

        self.PARAMFRAME = Frame(root)
        self.PARAMFRAME.pack(side=TOP)

        scrollbar = Scrollbar(self.PARAMFRAME)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.RESULTLIST = Listbox(self.PARAMFRAME, width=120, height=50,yscrollcommand=scrollbar.set)
        self.RESULTLIST.pack(side=LEFT)


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()