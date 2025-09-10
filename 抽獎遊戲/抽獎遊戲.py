import numpy as np
import pandas as pd
import random
random.seed(123)

print('模擬次數=2000','每輪抽獎次數=1000',sep='\n')
results = [] 
for First_Prize in range(100,2000,50):
    for Second_Prize in range(50,First_Prize,50):

        MSE = 0
        EX = 45
        for k in range(1000):
            Lottery_result_order_lst = []
            count = 0
            for i in range(2000):
                if len(Lottery_result_order_lst) > 0 and Lottery_result_order_lst[-1] != 0: 
                    Prize = np.random.choice([0,1,2], p=[0.925,0.025,0.05])
                else:
                    Prize = np.random.choice([0,1,2], p=[0.85,0.05,0.1]) 

                if i == 4 and sum(Lottery_result_order_lst) == 0:
                    Prize = np.random.choice([1,2],size=1,p=[0.33,0.67])[0]

                if Prize == 0:
                    count += 1
                    if count == 19:
                        Prize = np.random.choice([1,2],size=1,p=[0.33,0.67])[0]
                else:
                    count = 0
                    
                Lottery_result_order_lst.append(Prize)

            # 用新清單轉換，不要覆蓋
            prize_map = {
                0: 0,
                1: First_Prize,
                2: Second_Prize,
            }
            mapped_lst = [prize_map[x] for x in Lottery_result_order_lst]
            ex = np.average(mapped_lst)
            MSE += (EX - ex)**2
        avg_mse = MSE/1000
        results.append([First_Prize, Second_Prize, avg_mse])
        print(f'First_Prize= {First_Prize} , Second_Prize= {Second_Prize}')
        print('MSE:', avg_mse)
        

# 轉成 DataFrame
df = pd.DataFrame(results, columns=['First_Prize', 'Second_Prize', 'MSE'])
# 存成 CSV
df.to_csv("/Users/ray/Desktop/抽獎遊戲.csv", index=False, encoding="utf-8-sig")

print('最小誤差：')
print(df[df['MSE']==df['MSE'].min()])