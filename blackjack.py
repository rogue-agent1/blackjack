#!/usr/bin/env python3
"""blackjack - Blackjack simulator."""
import sys,argparse,json,random
def deck():return[(r,s) for r in range(1,14) for s in "shdc"]
def value(hand):
    total=0;aces=0
    for r,_ in hand:
        if r==1:aces+=1;total+=11
        elif r>=10:total+=10
        else:total+=r
    while total>21 and aces:total-=10;aces-=1
    return total
def play(strategy="basic"):
    d=deck()*6;random.shuffle(d)
    player=[d.pop(),d.pop()];dealer=[d.pop(),d.pop()]
    while value(player)<17 if strategy=="basic" else value(player)<12:
        player.append(d.pop())
    while value(dealer)<17:dealer.append(d.pop())
    pv,dv=value(player),value(dealer)
    if pv>21:return "lose"
    if dv>21:return "win"
    if pv>dv:return "win"
    if pv<dv:return "lose"
    return "push"
def main():
    p=argparse.ArgumentParser(description="Blackjack")
    p.add_argument("--games",type=int,default=1000)
    p.add_argument("--strategy",choices=["basic","conservative"],default="basic")
    args=p.parse_args()
    from collections import Counter
    results=Counter(play(args.strategy) for _ in range(args.games))
    print(json.dumps({"games":args.games,"strategy":args.strategy,"wins":results["win"],"losses":results["lose"],"pushes":results["push"],"win_rate":round(results["win"]/args.games*100,1),"house_edge":round((results["lose"]-results["win"])/args.games*100,2)},indent=2))
if __name__=="__main__":main()
