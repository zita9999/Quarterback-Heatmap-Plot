# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import requests
import urllib.request
import time
import bs4 as bs
import pandas as pd
import seaborn as sns
import numpy as np



#input variables
Player_first = input('Players First Name:')
Player_first = Player_first.title() 
Player_last = input('Players Last Name:')
Player_last = Player_last.title()
year = input('Which Year:')


f2 = Player_first[0:2]
l4 = Player_last[0:4]


#webscraping the plays/stats for the inputed quarterback for weeks 1-8
url = 'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&player_id_hint='+Player_first+'+'+Player_last+'&player_id_select='+Player_first+'+'+Player_last+'&player_id='+l4+f2+'00&idx=players_pbp&year_min='+year+'&year_max='+year+'&game_type=R&game_num_min=0&game_num_max=99&week_num_min=1&week_num_max=8&quarter%5B%5D=1&quarter%5B%5D=2&quarter%5B%5D=3&quarter%5B%5D=4&quarter%5B%5D=5&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D=0&down%5B%5D=1&down%5B%5D=2&down%5B%5D=3&down%5B%5D=4&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=PASS&type%5B%5D=RUSH&type%5B%5D=PUNT&type%5B%5D=KOFF&type%5B%5D=ONSD&type%5B%5D=FG&type%5B%5D=XP&type%5B%5D=2PC&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&rush_direction%5B%5D=LE&rush_direction%5B%5D=LT&rush_direction%5B%5D=LG&rush_direction%5B%5D=M&rush_direction%5B%5D=RG&rush_direction%5B%5D=RT&rush_direction%5B%5D=RE&pass_location%5B%5D=SL&pass_location%5B%5D=SM&pass_location%5B%5D=SR&pass_location%5B%5D=DL&pass_location%5B%5D=DM&pass_location%5B%5D=DR&order_by=game_date&order_by_asc=Y'
html = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(html, 'lxml')
table = soup.find('div', id = 'div_all_plays')

#this gets the team of the player
teams = soup.find('div', id = 'all_tm_offense')
team = teams.text.split()
team = team[-1]
team = team[0:3]
team


labels = []
data = []
rows = table.find_all('tr')

for row in rows:
    labels.append(str(row.find_all('td')[8:9]))

#webscraping plays for weeks 9-17
url2 = 'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&player_id_hint='+Player_first+'+'+Player_last+'&player_id_select='+Player_first+'+'+Player_last+'&player_id='+l4+f2+'00&idx=players_pbp&year_min='+year+'&year_max='+year+'&game_type=R&game_num_min=0&game_num_max=99&week_num_min=9&week_num_max=17&quarter%5B%5D=1&quarter%5B%5D=2&quarter%5B%5D=3&quarter%5B%5D=4&quarter%5B%5D=5&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D=0&down%5B%5D=1&down%5B%5D=2&down%5B%5D=3&down%5B%5D=4&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=PASS&type%5B%5D=RUSH&type%5B%5D=PUNT&type%5B%5D=KOFF&type%5B%5D=ONSD&type%5B%5D=FG&type%5B%5D=XP&type%5B%5D=2PC&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&rush_direction%5B%5D=LE&rush_direction%5B%5D=LT&rush_direction%5B%5D=LG&rush_direction%5B%5D=M&rush_direction%5B%5D=RG&rush_direction%5B%5D=RT&rush_direction%5B%5D=RE&pass_location%5B%5D=SL&pass_location%5B%5D=SM&pass_location%5B%5D=SR&pass_location%5B%5D=DL&pass_location%5B%5D=DM&pass_location%5B%5D=DR&order_by=game_date&order_by_asc=Y'
html2 = urllib.request.urlopen(url2).read()

soup = bs.BeautifulSoup(html2, 'lxml')
table = soup.find('div', id = 'div_all_plays')

labels2 = []
data = []
rows = table.find_all('tr')

for row in rows:
    labels2.append(str(row.find_all('td')[8:9]))
    
#all this above is webscraping to get the data
    


#everything below is seperating the plays into different Series/Dataframes
#they will show completed/incompleted/interceptions for each part of the field
df1 = pd.DataFrame(labels)
df2 = pd.DataFrame(labels2)
df = pd.concat([df1,df2])
df = df[1:]
df['Complete'] = 0
df['Incomplete'] = 0
df['Short Middle'] = 0
df['Short Left'] = 0
df['Short Right'] = 0
df['Deep Middle'] = 0
df['Deep Left'] = 0
df['Deep Right'] = 0
df['Intercepted'] = 0

touchdowns = 0
for rows in df[0]:
    if 'pass' in rows:
        if 'touchdown' in rows and 'intercepted' not in rows:
            touchdowns+=1
        

counter = -1
for rows in df[0]:
    counter += 1
    if 'pass' in rows:
        if 'intercepted' in rows:
            df.iloc[counter,9] = 1
        elif 'incomplete' in rows:
            df.iloc[counter,2] = 1
        else:
            df.iloc[counter,1] = 1
        
        
    if 'short middle' in rows:
        df.iloc[counter,3] = 1
    if 'short right' in rows:
        df.iloc[counter,5] = 1
    if 'short left' in rows:
        df.iloc[counter,4] = 1
    if 'deep middle' in rows:
        df.iloc[counter,6] = 1
    if 'deep left' in rows:
        df.iloc[counter,7] = 1
    if 'deep right' in rows:
        df.iloc[counter,8] = 1


        

#Short Middle
mark1 = (df['Short Middle'] == 1)
mark2 = (df['Complete'] == 1)
mark3 = (df['Incomplete']==1)

sm_complete = df[mark1 & mark2]
sm_incomplete = df[mark1 & mark3]
total_sm = df['Short Middle'].sum()
    
#Short Left  
mark4 = (df['Short Left'] == 1)
mark5 = (df['Complete'] == 1)
mark6 = (df['Incomplete']==1)

sl_complete = df[mark4 & mark5]
sl_incomplete = df[mark4 & mark6]
total_sl = df['Short Left'].sum()

#Short Right
mark7 = (df['Short Right'] == 1)
mark8 = (df['Complete'] == 1)
mark9 = (df['Incomplete']==1)

sr_complete = df[mark7 & mark8]
sr_incomplete = df[mark7 & mark9]
total_sr = df['Short Right'].sum()   
        
#Deep Middle
mark10 = (df['Deep Middle'] == 1)
mark11 = (df['Complete'] == 1)
mark12 = (df['Incomplete']==1)

dm_complete = df[mark10 & mark11]
dm_incomplete = df[mark10 & mark12]
total_dm = df['Deep Middle'].sum() 

#Deep Right
mark13 = (df['Deep Right'] == 1)
mark14 = (df['Complete'] == 1)
mark15 = (df['Incomplete']==1)

dr_complete = df[mark13 & mark14]
dr_incomplete = df[mark13 & mark15]
total_dr = df['Deep Right'].sum()

#Deep Left
mark16 = (df['Deep Left'] == 1)
mark17 = (df['Complete'] == 1)
mark18 = (df['Incomplete']==1)

dl_complete = df[mark16 & mark17]
dl_incomplete = df[mark16 & mark18]
total_dl = df['Deep Left'].sum()

#interceptions
sm_intercepted = df[(df['Intercepted'] ==1) & (df['Short Middle']==1)]
sl_intercepted = df[(df['Intercepted'] ==1) & (df['Short Left']==1)]
sr_intercepted = df[(df['Intercepted'] ==1) & (df['Short Right']==1)]
dm_intercepted = df[(df['Intercepted'] ==1) & (df['Deep Middle']==1)]
dl_intercepted = df[(df['Intercepted'] ==1) & (df['Deep Left']==1)]
dr_intercepted = df[(df['Intercepted'] ==1) & (df['Deep Right']==1)]


#creating the final dataframe that will show the summaries of the passes thrown in each part of the field
smc = sm_complete['Complete'].sum()
smi = sm_incomplete['Incomplete'].sum()
smin = sm_intercepted['Intercepted'].sum()

src = sr_complete['Complete'].sum()
sri = sr_incomplete['Incomplete'].sum()
srin = sr_intercepted['Intercepted'].sum()

slc = sl_complete['Complete'].sum()
sli = sl_incomplete['Incomplete'].sum()
slin = sl_intercepted['Intercepted'].sum()

dmc = dm_complete['Complete'].sum()
dmi = dm_incomplete['Incomplete'].sum()
dmin = dm_intercepted['Intercepted'].sum()

dlc = dl_complete['Complete'].sum()
dli = dl_incomplete['Incomplete'].sum()
dlin = dl_intercepted['Intercepted'].sum()

drc = dr_complete['Complete'].sum()
dri = dr_incomplete['Incomplete'].sum()
drin = dr_intercepted['Intercepted'].sum()
 
data = {'Short Middle':[smc,smi,total_sm,smin],
        'Short Left': [slc,sli,total_sl,slin],
        'Short Right': [src,sri,total_sr,srin],
        'Deep Middle': [dmc,dmi,total_dm,dmin],
        'Deep Left': [dlc,dli,total_dl,dlin],
        'Deep Right': [drc,dri,total_dr,drin]}


final_df = pd.DataFrame(data, index = ['Complete', 'Incomplete', 'Total Passes', 'Intercepted'])



#determining the colour of the heatmap based on the played for team

if team == 'PHI':
    h_color = 'Greens'
    name = 'Eagles'
elif team == 'DAL':
    h_color = 'Blues'
    name = 'Cowboys'
elif team == 'CHI':
    h_color = 'Oranges'
    name = 'Bears'
elif team == 'BUF':
    h_color = 'Blues'
    name = 'Bills'
elif team == 'DET':
    h_color = 'Blues'
    name = 'Lions'
elif team == 'GNB':
    h_color = 'Greens'
    name = 'Packers'
elif team == 'MIA':
    h_color = 'YlGn'
    name = 'Doplhins'
elif team == 'MIN':
    h_color = 'Purples'
    name = 'Vikings'
elif team == 'NOR':
    h_color = 'YlOrBr'
    name = 'Saints'
elif team == 'NWE':
    h_color = 'Blues'
    name = 'Patriots'
elif team == 'NYG':
    h_color = 'Blues'
    name = 'Giants'
elif team == 'NYJ':
    h_color = 'Greens'
    name = 'Jets'
elif team == 'LAR':
    h_color = 'Blues'
    name = 'Rams'
elif team == 'WAS':
    h_color = 'Reds'
    name = 'Redskins'
elif team == 'CIN':
    h_color = 'Oranges'
    name = 'Bengals'
elif team == 'CLE':
    h_color = 'Oranges'
    name = 'Browns'
elif team == 'HOU':
    h_color = 'Blues'
    name = 'Texans'
elif team == 'KAN':
    h_color = 'Reds'
    name = 'Chiefs'
elif team == 'PIT':
    h_color = 'YlOrRd'
    name = 'Steelers'
elif team == 'BAL':
    h_color = 'Purples'
    name = 'Ravens'
elif team == 'SEA':
    h_color = 'GnBu'
    name = 'Seahawks'
elif team == 'ATL':
    h_color = 'Reds'
    name = 'Falcons'
elif team == 'CAR':
    h_color = 'Blues'
    name = 'Panthers'
elif team == 'ARI':
    h_color = 'Reds'
    name = 'Cardinals'
elif team == 'SFO':
    h_color = 'YlRd'
    name = '49ers'
elif team == 'TAM':
    h_color = 'OrRd'
    name = 'Buccaneers'
elif team == 'IND':
    h_color = 'Blues'
    name = 'Colts'
elif team == 'JAX':
    h_color = 'YlGnBu_R'
    name = 'Jaguars'
elif team == 'OAK':
    h_color = 'Greys'
    name = 'Raiders'
elif team == 'LAC':
    h_color = 'YlGnBu'
    name = 'Chargers'
elif team == 'TEN':
    h_color = 'Blues'
    name = 'Titans'
elif team =='DEN':
    h_color = 'Oranges'
    name = 'Broncos'

else:
    h_color = 'Blues'


#getting the completion percentage of each part of the field                     
sm_percentage = str(((smc/total_sm)*100).round(2))
sl_percentage = str(((slc/total_sl)*100).round(2)) 
sr_percentage = str(((src/total_sr)*100).round(2))       
dm_percentage = str(((dmc/total_dm)*100).round(2))    
dl_percentage = str(((dlc/total_dl)*100).round(2))
dr_percentage = str(((drc/total_dr)*100).round(2))
                       

#below is generating the points in the specified zones that the heatmap will use

from random import seed
from random import randint

#sm
sm_x = []
sm_y = []
i=1
while i <= total_sm:
    valuex = randint(20,40)
    valuey = randint(20,45)
    sm_x.append(valuex)
    sm_y.append(valuey)
    i+=1
#sl
sl_x = []
sl_y = []
i=1
while i <= total_sl:
    valuex = randint(0,20)
    valuey = randint(20,45)
    sl_x.append(valuex)
    sl_y.append(valuey)
    i+=1
    
#sr
sr_x = []
sr_y = []
i=1
while i <= total_sr:
    valuex = randint(40,60)
    valuey = randint(20,45)
    sr_x.append(valuex)
    sr_y.append(valuey)
    i+=1

#dm
dm_x = []
dm_y = []
i=1
while i <= total_dm:
    valuex = randint(20,40)
    valuey = randint(55,85)
    dm_x.append(valuex)
    dm_y.append(valuey)
    i+=1

#dr
dr_x = []
dr_y = []
i=1
while i <= total_dr:
    valuex = randint(40,60)
    valuey = randint(55,85)
    dr_x.append(valuex)
    dr_y.append(valuey)
    i+=1

#dl
dl_x = []
dl_y = []
i=1
while i <= total_dl:
    valuex = randint(0,20)
    valuey = randint(55,85)
    dl_x.append(valuex)
    dl_y.append(valuey)
    i+=1


X_axis = sm_x +sr_x + sl_x + dr_x + dm_x + dl_x+[20]+[40]
Y_axis = sm_y + sr_y + sl_y + dr_y + dl_y + dm_y+[0] +[110]

X_axis = np.array(X_axis)
Y_axis = np.array(Y_axis)


#web scraping the picture of the player from pro-football-reference
t = l4[0]

url_photo = 'https://www.pro-football-reference.com/players/'+t+'/'+l4+f2+'00.htm'

html4 = urllib.request.urlopen(url_photo).read()

soup = bs.BeautifulSoup(html4, 'lxml')


for img in soup.find_all('img'):
        print(img)
        temp = (img.get('src'))
        print(temp)
        if l4 in temp:
            photo = temp
            
            
            
#im downloading the image and saving it in my files and opening it up again and changing it to a png
#this is the only way the image works, otherwise its corrupted
imagefile = open('Last_Player_Image' + '.jpg', 'wb')
imagefile.write(urllib.request.urlopen(photo).read())
imagefile.close()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = Image.open('C:/Users/chris/OneDrive/Documents/Courses and Projects/Last_Player_Image.jpg')

img.save('ImgPlayer.png')
img.close()
img = mpimg.imread('file:///C:/Users/chris/OneDrive/Documents/Courses and Projects/ImgPlayer.png')
img



#getting the logo of the team
lower_team = team.lower()
url_photo2 = 'https://www.pro-football-reference.com/teams/'+lower_team+'/'

html5 = urllib.request.urlopen(url_photo2).read()

soup = bs.BeautifulSoup(html5, 'lxml')


for img2 in soup.find_all('img'):
        temp = (img2.get('src'))
        if 'tlogo' in temp:
            logo = temp


imagefile2 = open('Logo' + '.jpg', 'wb')
imagefile2.write(urllib.request.urlopen(logo).read())
imagefile2.close()


img2 = Image.open('C:/Users/chris/OneDrive/Documents/Courses and Projects/Logo.jpg')
img2.save('L.png')
img2.close()
img2 = mpimg.imread('file:///C:/Users/chris/OneDrive/Documents/Courses and Projects/L.png')




#creating the football field

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import plotly.graph_objects as go
import turtle

fig=plt.figure()
fig.set_size_inches(14,13)
ax=fig.add_subplot(1,2,1)

plt.plot([0,0],[0,110], color="black", linewidth = 5)
plt.plot([0,60],[110,110], color="black", linewidth = 5)
plt.plot([60,60],[110,0], color="black", linewidth = 5)
plt.plot([60,0],[0,0], color="black", linewidth = 5)
plt.plot([0,60],[20,20], color="blue")
plt.plot([0,60],[95,95], color="black")

#Creating the sections

plt.plot([0,60],[45,45], color = 'black')
#Short 
plt.plot([20,20],[20,45], color = 'black')
plt.plot([40,40],[20,45], color = 'black')
#Deep
plt.plot([20,20],[45,95], color = 'black')
plt.plot([40,40],[45,95], color = 'black')

#putting the heatmap on top of our field
sns.kdeplot(X_axis,Y_axis,shade = 'True', n_levels = 500,
            shade_lowest = True, cmap = h_color)
            
plt.ylim(0,110)
plt.xlim(0,60)


#texts within the plot
ax.text(12,104, Player_first, fontsize = 38, fontweight = 'bold',
        horizontalalignment = 'left', color = 'black')

ax.text(12,98, Player_last, fontsize = 38, fontweight = 'bold',
        horizontalalignment = 'left', color = 'black')

ax.text(30, 16, 'Line of Scrimmage (LOS)', fontsize = 18,
        horizontalalignment = 'center', color = 'blue')


ax.text(30,46, '15 yards from LOS', fontsize = 10, color = 'black',
        horizontalalignment = 'center')
#dl
ax.text(10,80, 'Completion %', fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(10,76,dl_percentage,fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(10,60,'Interceptions',fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(10,56, str(dlin),fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

#dm
ax.text(30,80, 'Completion %', fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(30,76,dm_percentage,fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(30,60,'Interceptions',fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(30,56, str(dmin),fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

#dr
ax.text(50,80, 'Completion %', fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(50,76,dr_percentage,fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(50,60,'Interceptions',fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(50,56, str(drin),fontsize = 13, color = 'black',
        horizontalalignment = 'center', fontweight = 'bold')

#sl
ax.text(10,38, 'Completion %', fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(10,34,sl_percentage,fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(10,26,'Interceptions',fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(10,22, str(slin),fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

#sm
ax.text(30,38, 'Completion %', fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(30,34,sm_percentage,fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(30,26,'Interceptions',fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(30,22, str(smin),fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

#sr
ax.text(50,38, 'Completion %', fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(50,34,sr_percentage,fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(50,26,'Interceptions',fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(50,22, str(srin),fontsize = 13, color = 'white',
        horizontalalignment = 'center', fontweight = 'bold')

ax.text(1,93,'Passes Thrown: ' + str(total_dl),fontsize = 9, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(21,93,'Passes Thrown: ' + str(total_dm),fontsize = 9, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(41,93,'Passes Thrown: ' + str(total_dr),fontsize = 9, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(1,43,'Passes Thrown: ' + str(total_sl),fontsize = 9, 
        color = 'white',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(21,43,'Passes Thrown: ' + str(total_sm),fontsize = 9, 
        color = 'white',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(41,43,'Passes Thrown: ' + str(total_sr),fontsize = 9, 
        color = 'white',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(1,11,'Touchdowns: ' + str(touchdowns),fontsize = 13, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

cmplt = (((smc+slc+src+dlc+drc+dmc)/(total_dm+total_dl+total_dr+total_sm+total_sr+total_sl))*100).round(2)

ax.text(1,8,'Total Completion%: ' + str(cmplt),fontsize = 13, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

total_int = drin +dmin+dlin+smin+srin+slin

ax.text(1,5,'Total Interceptions: ' + str(total_int),fontsize = 13, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(41,11,'Year: ' + str(year),fontsize = 13, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(41,8,'Team:' ,fontsize = 13, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

ax.text(41,5,name,fontsize = 13, 
        color = 'black',
        horizontalalignment = 'left', fontweight = 'bold')

#below is putting the image of the player and logo onto the plot

newax = fig.add_axes([0.088, 0.779,0.1,0.1], anchor = 'NE', zorder =10 )
newax.imshow(img)


newax2 = fig.add_axes([0.413, 0.815,0.06,0.06], anchor = 'NE', zorder =5 )
newax2.imshow(img2)
newax2.axis('off')
newax.axis('off')
ax.axis('off')

plt.savefig('Final_Image.png', bbox_inches = 'tight')
plt.show()








