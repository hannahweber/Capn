def predictor(injuryDf,playerDf,injuryKind=None,allstar=None,games=None,position=None,agg=None,repeated=None):
    import pandas as pd
    pd.set_option('display.max_columns', 500)
    import matplotlib.pyplot as plt
    import seaborn as sb
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    if games==None:
        games=4
    else:
        games+=1
    biggest = []
    s = ""
    if position!=None:
        if position == 'G':
            playerDf = playerDf[playerDf['playPos']==position].append(playerDf[playerDf['playPos']=='PG']).append(playerDf[playerDf['playPos']=='SG'])
        elif position =='F':
            playerDf = playerDf[playerDf['playPos']==position].append(playerDf[playerDf['playPos']=='PF']).append(playerDf[playerDf['playPos']=='SF'])
        else:
            playerDf = playerDf[playerDf['playPos']==position]
        s+="position = "+'\033[1m'+position+'\033[0m'
    else:
        s+="position = "+'\033[1m'+"all"+'\033[0m'
    if allstar!=None:
        playerDf = playerDf[playerDf['allstar']==allstar]
        if len(s)!=0:
            s+=", "
        s+="allstar = "+'\033[1m'+str(allstar)+'\033[0m'
    if games !=None:
        if len(s)!=0:
            s+=", "
        s+="games = "+'\033[1m'+str(games)+'\033[0m'
    if repeated !=None:
        if len(s)!=0:
            s+=", "
        s+="repeated = "+'\033[1m'+str(repeated)+'\033[0m'
    
    if injuryKind == None:
        if len(s)!=0:
            s+=", "
        s+="injuryKind = "+'\033[1m'+"all"+'\033[0m'
        #print("No injury specified")
        print('\033[1m'+"Testing:"+'\033[0m'+" "+s+"\n")
        print("Testing using data from",'\033[1m'+str(len(playerDf))+'\033[0m',"games.\n")
        for typeof in injuryDf['Notes'].value_counts()[1:13].index: # For each type of injury
            df_injury = injuryDf[injuryDf['Notes']==typeof] #               Then filter the df
            biggest.append(getBigger(typeof,df_injury,playerDf,repeated))
            
    else:
        if len(s)!=0:
            s+=", "
        s+="injuryKind = "+'\033[1m'+injuryKind+'\033[0m'
        print('\033[1m'+"Testing:"+'\033[0m'+" "+s+"\n")
        print("Testing using data from",'\033[1m'+str(len(playerDf))+'\033[0m',"games.\n")
        #print(len(injuryDf),len(injuryDf[injuryDf['Notes']=='elbow']))
        biggest.append(getBigger(injuryKind,injuryDf[injuryDf['Notes']==injuryKind],playerDf,repeated))
    quant = 0.0000000000001
    #try:
    for i in biggest:
        for key, value in i.items():
            for j in value:
                if j[0] in range(games):
                    if quant>=10:
                        o = j[0]+1
                    else:
                        o=j[0]
                    if j[0]==1:
                        quant+=1
                        #print(j[0])
                    elif str(quant)[o]=='9':
                        pass
                        #print('pass',o)
                    else:
                        #print(j[0],.1**(j[0]-1))
                        quant+=.1**(j[0]-1)
    quant = float(str(quant)[:games+1])

    #except:
        #print("broke",j[0],.1**(j[0]-1))
    #pass
    if quant==0:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThere is no data available based off of the inputted parameters. Try expanding your search parameters.\n")
    elif quant<=5:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThe data could be somewhat unreliable. Try expanding parameters, or know that this may not be the best predictor for this case.\n")
    elif quant<=10:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThe data should be somewhat accurate, due to not a ton available.\n")
    else:
        print('\033[1m'+"Score:"+'\033[0m',quant,"\nThe data should be pretty accurate.\n")
    if agg:

        points=0
        c = 0
        for kind in biggest:
            for key,value in kind.items():
                for i in value:
                    if i[0]>0 and i[0]<games:
                        points+=3*i[-8]
                        points+=2*i[-7]
                        points+=float(i[-6])
                        points+=1.2*i[-5]
                        points+=1.5*i[-4]
                        points+=2*i[-3]
                        points+=2*i[-2]
                        points-=i[-1]
                        c+=1
        return points/c
    else:
        d={}
        for kind in biggest:
            for key,value in kind.items():
                for i in value:
                    if i[0]>0 and i[0]<games:
                        points=0
                        points+=3*i[-8]
                        points+=2*i[-7]
                        points+=float(i[-6])
                        points+=1.2*i[-5]
                        points+=1.5*i[-4]
                        points+=2*i[-3]
                        points+=2*i[-2]
                        points-=i[-1]
                        try:
                            d[i[0]][0]+=points
                            d[i[0]][1]+=1
                        except:
                            d[i[0]]=[0,0]
                            d[i[0]][0]+=points
                            d[i[0]][1]+=1
        for key,value in d.items():
            if key==1:
                key = '1st'
            elif key==2:
                key='2nd'
            elif key==3:
                key='3rd'
            else:
                key=str(key)+'th'
            print("On the",'\033[1m'+"'{0}'".format(key)+'\033[0m',"game, we predict",'\033[1m'+"'{0}'".format(value[0]/value[1])+'\033[0m',"points.")

def getBigger(ij,injuryDf,playerDf,repeated=None):
    #print("here",len(injuryDf))
    import pandas as pd
    pd.set_option('display.max_columns', 500)
    import matplotlib.pyplot as plt
    import seaborn as sb
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    df = playerDf
    bigger = []
    #count
    for player in injuryDf['Relinquised'].unique():  # For each player in injuries df
            player_injuries = [t for t in injuryDf[injuryDf['Relinquised']==player]['Date']]
            if repeated==True:
                #print(player,"injury count:",len(player_injuries))
                player_injuries = player_injuries[1:]# Grab all the dates of said players injuries
            elif repeated==False:
                player_injuries = player_injuries[:1]
            #if len(player_injuries)==0:
            #    print("Player does not have any recorded injuries:",player)
            #try:
            ln = player.split()[1] # Players df holds names in two different categories
            fn = player.split()[0]
            for i in range(len(player_injuries)): # For each injury that player had
                #print(player,player_injuries[i])
                date = player_injuries[i]    #      Find date of injury
                if i!=0:                         #      We need to set a date of previous injury, if there is one
                    dateM1 = player_injuries[i-1] # If we can find it, we set it
                else:
                    dateM1 = pd.to_datetime("1990-01-01")# If we can't, we set previous date until way in the past
                if i+1!=len(player_injuries):
                    dateP1 = player_injuries[i+1] # Same for next injury
                else:
                    dateP1 = pd.to_datetime("2090-01-01")

                b = df[df['playLNm']==ln] # Find that players games
                b = b[b['playFNm']==fn].reset_index()
                #print(len(b))
                #b = players[players['playDispNm']==player].reset_index() # Find that players games
                if len(b>0):
                    #print(len(b),"matches found for player name",fn,ln)
                    pass
                else:
                    pass
                    #nmf.append(player)
                    #print("No matches found for player name",fn,ln)
                    
                if len(b[b['gmDate']==date])>0: # This is testing if the injury happened during a game
                    #print("player","here here")
                    g = 1
                    game_injury_index = b[b['gmDate']==date].index[0]
                    #print("During game")

                #else:
                    #Injury did not happen during a game if it got here, so pass (aka discard)
                    #pass
                    for daterange in range(game_injury_index-6,game_injury_index):
                        try:
                            row = b.loc[daterange] # Grab a specific row
                            if row.gmDate >dateM1: # Making sure that the game wasn't prior to a different injury
                                pre = [daterange-game_injury_index,row.gmDate,row.playPTS,row.playMin,row.playAST,row.play2PM,row.play3PM,row.playFTM,row.playORB,row.playDRB,row.playAST,row.playBLK,row.playSTL,row.playTO] # Build a list of useful info
                                bigger.append(pre)# Add list to bigger list
                                #print(player,"added")
                                #print("added")
                        except:# If we get to this point, it means it couldnt find a previous game of that number
                            #print("row")
                            print(player,"NOT added")
                            if typeof=='wrist':
                                #print(daterange,date,fn,ln,game_injury_index)
                                pass # E.g. It couldnt find the 7th previous game to the injury

                        try:
                            row = b.loc[daterange+6+g]
                            if row.gmDate<dateP1: # Same as above, but with games AFTER injury
                                post = [daterange-game_injury_index+7,row.gmDate,row.playPTS,row.playMin,row.playAST,row.play2PM,row.play3PM,row.playFTM,row.playORB,row.playDRB,row.playAST,row.playBLK,row.playSTL,row.playTO]
                                bigger.append(post)
                        except: # Same as above except statement
                            pass
                else:
                    for w in range(0,365):
                        if len(b[b['gmDate']==date-pd.Timedelta(w,'d')])>0:
                            game_injury_index = b[b['gmDate']==date-pd.Timedelta(w,'d')].index[0]
                            for daterange in range(game_injury_index-5,game_injury_index+1):
                                try:
                                    row = b.loc[daterange] # Grab a specific row
                                    if row.gmDate >dateM1: # Making sure that the game wasn't prior to a different injury
                                        pre = [daterange-game_injury_index-1,row.gmDate,row.playPTS,row.playMin,row.playAST,row.play2PM,row.play3PM,row.playFTM,row.playORB,row.playDRB,row.playAST,row.playBLK,row.playSTL,row.playTO] # Build a list of useful info
                                        bigger.append(pre)# Add list to bigger list
                                        #print(player)
                                except:# If we get to this point, it means it couldnt find a previous game of that number
                                    pass
                                    #print("row")
                                    #if typeof=='wrist':
                                    #    print(daterange,date,fn,ln,game_injury_index)
                                    #pass # E.g. It couldnt find the 7th previous game to the injury

                                try:
                                    row = b.loc[daterange+6]
                                    if row.gmDate<dateP1: # Same as above, but with games AFTER injury
                                        post = [daterange-game_injury_index+6,row.gmDate,row.playPTS,row.playMin,row.playAST,row.play2PM,row.play3PM,row.playFTM,row.playORB,row.playDRB,row.playAST,row.playBLK,row.playSTL,row.playTO]
                                        bigger.append(post)
                                except: # Same as above except statement
                                    pass
                            break
                #else:
                    #print("Injury did not happen during a game if it got here, so pass (aka discard)")
                    #print(i)
            #except:
                #print(player) # This means something weird happened, so print the players name
    #print({ij:bigger})
    #if [e,i for e,i in {ij:bigger}]
    return {ij:bigger}
