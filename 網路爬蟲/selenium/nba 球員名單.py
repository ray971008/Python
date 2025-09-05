# 球隊網址
import requests,os,csv,re,os
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://www.qiumiwu.com/standings'
HEADERS ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
data = requests.get(url,headers = HEADERS)
soup = BeautifulSoup(data.text,'html.parser')
item = soup.find_all('div',{'class':'bottom-content-list'})

# 球員網址
therf_list=[]
for i in item:
    herf=re.findall('href="(.*?)"' ,str(i))[0]
    herf = "http:"+herf+"/roster"
    therf_list.append(herf)
therf_list

pherf_list=[]
for j in therf_list:
    data = requests.get(j,headers = HEADERS)
    soup = BeautifulSoup(data.text,'html.parser')

    item = soup.find('div',{'class':'roster-info__player'})
    item1 = item.find_all('a',class_="roster-info__player-list roster-info__player-list--data")
    for k in item1:
        herf = re.findall('href="(.*?)"',str(k))[0]
        herf = 'http:'+herf+'/stat'
        pherf_list.append(herf)

# 建立 dataframe
df = pd.DataFrame([('0',"0","0",0,0,0,0,0,0,0,'0',0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)], 
                  columns=["Player", "team","位置", "背號","年薪","身高","年齡","體重","年資",
                           "臂展","國籍","先發場次","總場次","場均時間","場均得分","場均助攻","場均抄截","場均蓋帽","場均失誤","場均犯規", "場均進攻籃板","場均防守籃板","場均籃板","場均命中數","場均出手數",'場均命中率',"場均三分命中數","場均三分數",'場均三分率',"場均罰球命中數","場均罰球數","場均罰球命中率","真實命中率","有效命中率","籃板率","進攻籃板率","防守籃板率","助攻率","失誤率","三分占出手比率","罰球率","球權使用率","效率值","勝利貢獻值","進攻端正負值","防守端正負值"])
# 球隊網址
import requests,os,csv,re,os
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://www.qiumiwu.com/standings'
HEADERS ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
data = requests.get(url,headers = HEADERS)
soup = BeautifulSoup(data.text,'html.parser')
item = soup.find_all('div',{'class':'bottom-content-list'})

# 球員網址
therf_list=[]
for i in item:
    herf=re.findall('href="(.*?)"' ,str(i))[0]
    herf = "http:"+herf+"/roster"
    therf_list.append(herf)
therf_list

pherf_list=[]
for j in therf_list:
    data = requests.get(j,headers = HEADERS)
    soup = BeautifulSoup(data.text,'html.parser')

    item = soup.find('div',{'class':'roster-info__player'})
    item1 = item.find_all('a',class_="roster-info__player-list roster-info__player-list--data")
    for k in item1:
        herf = re.findall('href="(.*?)"',str(k))[0]
        herf = 'http:'+herf+'/stat'
        pherf_list.append(herf)

# 建立 dataframe
df = pd.DataFrame([('0',"0","0",0,0,0,0,0,0,0,'0',0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)], 
                  columns=["Player", "team","位置", "背號","年薪","身高","年齡","體重","年資", "臂展","國籍","先發場次","總場次","場均時間","場均得分","場均助攻","場均抄截","場均蓋帽","場均失誤","場均犯規", "場均進攻籃板","場均防守籃板","場均籃板","場均命中數","場均出手數",'場均命中率',"場均三分命中數","場均三分數",'場均三分率',"場均罰球命中數","場均罰球數","場均罰球命中率","真實命中率","有效命中率","籃板率","進攻籃板率","防守籃板率","助攻率","失誤率","三分占出手比率","罰球率","球權使用率","效率值","勝利貢獻值","進攻端正負值","防守端正負值"])
# 抓資料
count = 0
for k in range(1,100):
    r = pherf_list[k]
    data1 = requests.get(r,headers = HEADERS)
    soup1 = BeautifulSoup(data1.text,'html.parser')
    item1 = soup1.find('div',{'class':'header-info__basic'})
    name = item1.find('h2',class_="header-info__basic__name-box__alias").text # 姓名
    item2 = item1.find('span',class_="header-info__basic__rank__desc").text
    team = re.findall('(.+)\s.*\s',item2)[0] # 隊伍
    position = re.findall('\s(.+)\s',item2)[0] # 位置
    number = int(re.findall('\d+',item2)[0]) # 背號

    item5 = soup1.find('div',{'class':'header-info__info'}).find_all('span')
    salary = float(re.findall('(.*?)万美元',item5[3].text)[0])*(10**5) if item5[3].text !='-' else None # 薪水
    height = float(re.findall('\d+',item5[6].text)[0])  if item5[6].text !='-' else None# 身高
    yearold = float(re.findall('\d+',item5[8].text)[0]) if item5[8].text !='-' else None # 年齡
    wieght = float(re.findall('\d+',item5[10].text)[0]) if item5[10].text !='-' else None # 體重
    seniority = float(re.findall('\d+',item5[12].text)[0]) if item5[12].text !='-' else None # 年資
    wingspan = float(re.findall('\d+',item5[14].text)[0]) if item5[14].text != '-' else None # 臂展 
    country = item5[16].text # 國籍
    if  salary != None:
        print(count)
        item6 = soup1.find('div',class_='career-right custom_scrollbar horizontal')
        item7 = item6.find('div',class_='appearance column').find_all('div',class_='list')
        a = re.findall('<div>(.*)</div>',str(item7[2]))
        starts = int(a[0]) if a[0]!='-' else 0# 先發場次
        total_game = int(a[1]) if a[1]!='-' else 0# 總場次
        time = float(a[2]) if a[2]!='-' else 0# 場均時間

        item8 = item6.find('div',class_='basis column').find_all('div',class_='list')
        b = re.findall('<div>(.*)</div>',str(item8[2]))
        point  = float(b[0]) if b[0]!='-' else 0  # 場均得分
        assist  = float(b[1]) if b[1]!='-' else 0  # 場均助攻
        steal  = float(b[2]) if b[2]!='-' else 0 # 場均抄截
        block  = float(b[3]) if b[3]!='-' else 0  # 場均蓋帽
        mistake  = float(b[4]) if b[4]!='-' else 0  # 場均失誤
        foul  = float(b[5]) if b[5]!='-' else 0  # 場均犯規

        item9 = item6.find('div',class_='backboard column').find_all('div',class_='list')
        c = re.findall('<div>(.*)</div>',str(item9[2]))
        offensive_rebound = float(c[0])  if c[0]!='-' else 0# 場均進攻籃板
        defensive_rebound = float(c[1]) if c[1]!='-' else 0 # 場均防守籃板
        rebound = float(c[2]) if c[2]!='-' else 0# 場均籃板

        item10 = item6.find('div',class_='shot column').find_all('div',class_='list')
        d = re.findall('<div>(.*)</div>',str(item10[2]))
        shot_goal = float(re.findall('(.*)/',d[0])[0]) if re.findall('(.*)/',d[0]) != '-' else None  # 場均命中數
        shot = float(re.findall('/(.*)',d[0])[0]) # 場均出手數
        shot_precent =round(float(re.findall('(.*?)%',d[1])[0])/100,3) # 場均命中率

        item11 = item6.find('div',class_='three_points column').find_all('div',class_='list')
        e = re.findall('<div>(.*)</div>',str(item11[2]))
        three_point_goal = re.findall('(.*)/',e[0])[0] # 場均三分命中數
        three_point_goal = 0 if three_point_goal =='-' else float(three_point_goal)
        three_point_shot = re.findall('/(.*)',e[0])[0] # 場均三分數
        three_point_shot = 0 if three_point_shot =='-' else float(three_point_shot)
        three_point_precent = 0 if e[1] =='-' else round(float(re.findall('(.*?)%',e[1])[0])/100,3)# 場均三分率
        
        item12 = item6.find('div',class_='penalty column').find_all('div',class_='list')
        f = re.findall('<div>(.*)</div>',str(item12[2]))
        free_throw_goal = re.findall('(.*)/',f[0])[0] # 場均罰球命中數
        free_throw_goal = 0 if free_throw_goal =='-' else float(free_throw_goal)
        free_throw = re.findall('/(.*)',f[0])[0]# 場均罰球數
        free_throw = 0 if free_throw =='-' else float(free_throw)
        free_throw_precent = 0 if f[1] =='-' else round(float(re.findall('(.*?)%',f[1])[0])/100,3)# 場均罰球命中率

        item4 = soup1.find('div',id='advanced-list').find_all('p')
        true_rate = round(float(re.findall('(.*?)%',item4[0].text)[0])/100,3)if item4[0].text != '-' else None # 真實命中率
        effective_rate = round(float(re.findall('(.*?)%',item4[1].text)[0])/100,3)if item4[1].text != '-' else None # 有效命中率
        rebound_rate = round(float(re.findall('(.*?)%',item4[2].text)[0])/100,3) if item4[2].text != '-' else None# 籃板率
        offensive_rebound_rate = round(float(re.findall('(.*?)%',item4[3].text)[0])/100,3)if item4[3].text != '-' else None # 進攻籃板率
        defensive_rebound_rate = round(float(re.findall('(.*?)%',item4[4].text)[0])/100,3)if item4[4].text != '-' else None  # 防守籃板率
        assist_rate = round(float(re.findall('(.*?)%',item4[5].text)[0])/100,3)if item4[5].text != '-' else None # 助攻率
        mistake_rate = round(float(re.findall('(.*?)%',item4[6].text)[0])/100,3)if item4[6].text != '-' else None # 失誤率
        three_point_shot_ratio = round(float(re.findall('(.*?)%',item4[7].text)[0])/100,3)if item4[7].text != '-' else None # 三分占出手比率
        free_throw_rate = round(float(re.findall('(.*?)%',item4[8].text)[0])/100,3)if item4[8].text != '-' else None # 罰球率
        usage_rate = round(float(re.findall('(.*?)%',item4[9].text)[0])/100,3)if item4[9].text != '-' else None # 球權使用率
        efficiency = round(float(item4[10].text),3)if item4[10].text != '-' else None # 效率值
        win_shares = round(float(item4[11].text),3) if item4[11].text != '-' else None # 勝利貢獻值
        offensive_plus_minus = round(float(item4[12].text),3) if item4[12].text != '-' else None # 進攻端正負值
        defensive_plus_minus = round(float(item4[13].text),3) if item4[13].text != '-' else None # 防守端正負值

        df.loc[count]=[name,team,position,number,salary,height, yearold,wieght,seniority,wingspan,country,starts,total_game,time,point,assist,steal,block,mistake,foul,offensive_rebound,defensive_rebound,rebound,shot_goal,shot,shot_precent,three_point_goal,three_point_shot,three_point_precent,free_throw_goal,free_throw,free_throw_precent, true_rate,effective_rate,rebound_rate,offensive_rebound_rate,defensive_rebound_rate,assist_rate,mistake_rate,three_point_shot_ratio,free_throw_rate,usage_rate,efficiency,win_shares,offensive_plus_minus,defensive_plus_minus]
        count+=1
os.chdir(r'/Users/ray/Downloads/python 程式檔/nba 資料')
df.to_excel('nba數據表.xlsx', index=False)
