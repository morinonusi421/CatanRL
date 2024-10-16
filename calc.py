import random
X = 10

kisu = []
gusu = []

for i in range(1,X+1):
    if i%2==0:
        gusu.append(i)
    else:
        kisu.append(i)

def battle():
    A_choice = random.sample(kisu,2)
    B_choice = random.sample(gusu,2)
    if max(A_choice) > max(B_choice):
        return "A"
    else:
        return "B"


#シミレーション回数
#大きくするほど正確だが，時間がかかる
NUM = 100000

Awin,Bwin = 0,0 
for i in range(NUM):
    if battle() == "A":
        Awin += 1
    else:
        Bwin += 1

print(f"Awin:{Awin},Bwin:{Bwin},Awin_rate:{Awin/NUM}")