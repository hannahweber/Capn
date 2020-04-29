import tkinter as tk
from graphics import *
import Tkinter
import time
from Tkinter import PhotoImage

from tkinter import *
from PIL import ImageTk, Image

def predictor(playerDf,injuryKind=None,allstar=None,games=None,position=None,agg=None,repeated=None,root=None,canvas=None):
    import pandas as pd
    pd.set_option('display.max_columns', 500)
    import matplotlib.pyplot as plt
    import seaborn as sb
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    ret = []
    if games==None:
        games=4
    else:
        games+=1
    biggest = []
    s = ""
    print(len(playerDf))
    if position!=None:
        playerDf = playerDf[playerDf['3']==position]
        s+="position = "+position+'\n'
    else:
        playerDf = playerDf[playerDf['3']!=playerDf['3']]
        s+="position = all"+'\n'
    print(len(playerDf))
    if allstar!=None:
        playerDf = playerDf[playerDf['1']==allstar]
        s+="allstar = "+str(allstar)+'\n'
    else:
        playerDf = playerDf[playerDf['1']!=playerDf['1']]
        s+="allstar = any"+'\n'
    if games !=None:
        s+="games = "+str(games)+'\n'
    print(len(playerDf))
    if repeated !=None:
        playerDf = playerDf[playerDf['4']==repeated]
        s+="repeated = "+str(repeated)+'\n'
    else:
        playerDf = playerDf[playerDf['4']!=playerDf['4']]
        s+="repeated = any"+'\n'
    
    if injuryKind == None:
        s+="injuryKind = all"+'\n'   
    else:
        print(len(playerDf))
        playerDf=playerDf[playerDf['0']==injuryKind]
        s+="injuryKind = "+injuryKind+'\n'
        
    if agg:
        print(len(playerDf))
        playerDf = playerDf[playerDf['5']==True]
        s+="agg = True"+'\n'
    else:
        print(len(playerDf))
        playerDf = playerDf[playerDf['5']==False]
        s+="agg = False"+'\n'
        
    print(len(playerDf))
    print('\033[1m'+"Testing:"+'\033[0m'+" "+s+"\n")
    #canvas.create_text(440,130,text="Testing:\n"+s, font = "-size 18")
    print("Testing using data from",'\033[1m'+str(len(playerDf))+'\033[0m',"games.\n")
    canvas.create_text(450,110,text="Testing using data\nfrom "+str(np.sum(playerDf['6']))+" games", font = "-size 18",fill='white')
        
    quant = np.sum(playerDf['7'])

    if quant==0:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThere is no data available based off of the inputted parameters. Try expanding your search parameters.\n")
        canvas.create_text(440,230,text="Score: "+str(quant)+"\nThere is no data\navailable based off\nof the inputted\nparameters. Try\nexpanding your search\nparameters.\n"+s, font = "-size 18")
    elif quant<=5:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThe data could be somewhat unreliable. Try expanding parameters, or know that this may not be the best predictor for this case.\n")
        canvas.create_text(440,230,text="Score: "+str(quant)+"\nThe data could be\nsomewhat unreliable. Try\nexpanding parameters,\nor know that this may\nnot be the best\npredictor for this\ncase.\n", font = "-size 18",fill='white')
    elif quant<=10:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThe data should be somewhat accurate, due to not a ton available.\n")
        canvas.create_text(440,230,text="Score: "+str(quant)+"\nThe data should be\npretty accurate,\ndue to some data\navailable.\n", font = "-size 18",fill='white')
    else:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThe data should be pretty accurate.\n")
        canvas.create_text(440,230,text="Score: "+str(quant)+"\nThe data should be\n accurate.\n", font = "-size 18",fill='white')
    if agg:
        m = "For the next "+str(games)+"games, we predict\n{0}".format(np.mean(playerDf['8']))+" points."

    else:
        d={}
        
        for key in range(8,12):
            if key==8:
                n = '1st'
            elif key==9:
                n='2nd'
            elif key==10:
                n='3rd'
            else:
                n=str(4)+'th'
            m = "On the {0} ".format(n)+"game, we predict\n{0}".format(np.mean(playerDf[str(key)]))+" points."
            print(m)
            canvas.create_text(440,270+40*(key-7),text=m, font = "-size 14",fill='white')

def loadIn():
    import pandas as pd
    pd.set_option('display.max_columns', 500)
    import matplotlib.pyplot as plt
    import seaborn as sb
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    #import color
    players = pd.read_csv("done2.csv")
    
    return players
    
#predictor(injuryDf = ij,playerDf = players, injuryKind ='elbow',position='C',games=4)

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))
    
def logInButton(e,canvas,root,d,players):
    print(e.x,e.y)
    if e.x>=105 and e.x<=445 and e.y<=510 and e.y>=450:
        
        if d['injury']=='Any':
            d['injury']=None
        else:
            d['injury']=d['injury'].lower()
        if d['position']=='Any':
            d['position']=None
        if d['agg']=='Any':
            d['agg']=None
        else:
            d['agg']=bool(d['agg'])
        if d['repeat']=='Any':
            d['repeat']=None
        else:
            d['repeat']=bool(d['repeat'])
        if d['allstar']=='Any':
            d['allstar']=None
        else:
            d['allstar']=bool(d['allstar'])
        print(d['injury'],d['position'],d['agg'],d['repeat'],d['allstar'])
        predictor(playerDf = players, injuryKind = d['injury'],position = d['position'],games=4,agg=d['agg'],repeated=d['repeat'],allstar = d['allstar'],canvas=canvas,root=root)

        
    
    elif e.x>=100 and e.x<=200 and e.y<=145 and e.y>=95:
        if d["injury"] == "Any":
            d["injury"] = "Knee"
        elif d["injury"] == "Knee":
            d["injury"] = "Ankle"
        elif d["injury"] == "Ankle":
            d["injury"] = "Back"
        elif d["injury"] == "Back":
            d["injury"] = "Foot"
        elif d["injury"] == "Foot":
            d["injury"] = "Hamstring"
        elif d["injury"] == "Hamstring":
            d["injury"] = "Calf"
        elif d["injury"] == "Calf":
            d["injury"] = "Hand"
        elif d["injury"] == "Hand":
            d["injury"] = "Concussion"
        elif d["injury"] == "Concussion":
            d["injury"] = "Head"
        elif d["injury"] == "Head":
            d["injury"] = "Wrist"
        elif d["injury"] == "Wrist":
            d["injury"] = "Elbow"
        elif d["injury"] == "Elbow":
            d["injury"] = "Illness"
        elif d["injury"] == "Illness":
            d["injury"] = "Rest"
        elif d["injury"] == "Rest":
            d["injury"] = "Any"
        else:
            d["injury"] = "Any"
        front(canvas,root,d,players)
    elif e.x>=100 and e.x<=200 and e.y<=215 and e.y>=165:
        if d["allstar"] == "Any":
            d["allstar"] = "True"
        elif d["allstar"] == "True":
            d["allstar"] = "False"
        else:
            d["allstar"] = "Any"
        front(canvas,root,d,players)
        
    elif e.x>=100 and e.x<=200 and e.y<=285 and e.y>=235:
        if d["repeat"] == "Any":
            d["repeat"] = "True"
        elif d["repeat"] == "True":
            d["repeat"] = "False"
        else:
            d["repeat"] = "Any"
        front(canvas,root,d,players)
    elif e.x>=100 and e.x<=200 and e.y<=355 and e.y>=305:
        if d["position"] == "Any":
            d["position"] = "G: All"
        elif d["position"] == "G: All":
            d["position"] = "SG"
        elif d["position"] == "SG":
            d["position"] = "PG"
        elif d["position"] == "PG":
            d["position"] = "F: All"
        elif d["position"] == "F: All":
            d["position"] = "PF"
        elif d["position"] == "PF":
            d["position"] = "SF"
        elif d["position"] == "SF":
            d["position"] = "C"
        elif d["position"] == "C":
            d["position"] = "Any"
        else:
            d["position"] = "Any"
        front(canvas,root,d,players)
    elif e.x>=100 and e.x<=200 and e.y<=425 and e.y>=375:
        if d["agg"] == "Any":
            d["agg"] = "True"
        elif d["agg"] == "True":
            d["agg"] = "False"
        else:
            d["agg"] = "Any"
        front(canvas,root,d,players)
    

def screen():
    d = {'allstar':'Any','injury':'Any','repeat':'Any','position':'Any','agg':'Any'}
    players = loadIn()
    root = tk.Tk()

    # --- create canvas with scrollbar ---

    canvas = tk.Canvas(root,width=650,height=600)
    canvas.pack(side=tk.LEFT)



    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side=tk.LEFT, fill='y')

    canvas.configure(yscrollcommand = scrollbar.set)

    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.bind('<Configure>', on_configure)

    # --- put frame in canvas ---

    frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=frame, anchor='nw')

    # --- add widgets in frame ---

    l = tk.Label(frame, text="Hello", font="-size 50")
    
    front(canvas,root,d,players)
    
    #canvas.bind("<Button-1>", lambda e: logInButton(e,canvas,root))
    canvas.pack()

    # --- start program ---
    root.mainloop()
    
def front(canvas,root,d,players):
    canvas.create_rectangle(55,30,595,550,fill='black') #Phone Border
    canvas.create_rectangle(65,50,585,530,fill='gray30') #Screen Border
    canvas.create_rectangle(105,450,445,510,fill='gray55') #Screen Border
    canvas.create_text(265,480,text="Run it!!!",fill='white',font='-size 32') #CU Intramurals
    
    canvas.create_rectangle(100,95,200,145,fill='gray75')
    canvas.create_text(150,120,text="Injury", font = "-size 22")
   
    canvas.create_rectangle(100,165,200,215,fill='gray75')
    canvas.create_text(150,190,text="Allstar", font = "-size 22")
    
    canvas.create_rectangle(100,235,200,285,fill='gray75')
    canvas.create_text(150,260,text="Repeat", font = "-size 22")
    
    canvas.create_rectangle(100,305,200,355,fill='gray75')
    canvas.create_text(150,330,text="Position", font = "-size 22")
    
    canvas.create_rectangle(100,375,200,425,fill='gray75')
    canvas.create_text(150,400,text="Agg", font = "-size 22")
    
    #------------------------------------------------------#
    
    canvas.create_rectangle(220,95,320,145,fill='lightblue')
    canvas.create_text(270,120,text=d["injury"], font = "-size 22")
   
    canvas.create_rectangle(220,165,320,215,fill='lightblue')
    canvas.create_text(270,190,text=d["allstar"], font = "-size 22")
    
    canvas.create_rectangle(220,235,320,285,fill='lightblue')
    canvas.create_text(270,260,text=d["repeat"], font = "-size 22")
    
    canvas.create_rectangle(220,305,320,355,fill='lightblue')
    canvas.create_text(270,330,text=d["position"], font = "-size 22")
    
    canvas.create_rectangle(220,375,320,425,fill='lightblue')
    canvas.create_text(270,400,text=d["agg"], font = "-size 22")
    
    canvas.bind("<Button-1>", lambda e: logInButton(e,canvas,root,d,players))
    
screen()