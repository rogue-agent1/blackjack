#!/usr/bin/env python3
"""Blackjack with basic strategy."""
import random
def new_deck():
    suits="SHDC";ranks="A23456789TJQK"
    deck=[(r,s) for s in suits for r in ranks];random.shuffle(deck);return deck
def hand_value(hand):
    val=0;aces=0
    for r,_ in hand:
        if r in "TJQK": val+=10
        elif r=="A": val+=11;aces+=1
        else: val+=int(r)
    while val>21 and aces: val-=10;aces-=1
    return val
def basic_strategy(player_hand,dealer_up):
    pv=hand_value(player_hand);dv={"A":11,"T":10,"J":10,"Q":10,"K":10}.get(dealer_up[0],int(dealer_up[0]))
    if pv>=17: return "stand"
    if pv>=13 and dv<=6: return "stand"
    if pv==12 and 4<=dv<=6: return "stand"
    if pv==11: return "double" if len(player_hand)==2 else "hit"
    if pv==10 and dv<=9: return "double" if len(player_hand)==2 else "hit"
    return "hit"
def play_hand(deck):
    if len(deck)<10: deck.extend(new_deck())
    player=[deck.pop(),deck.pop()];dealer=[deck.pop(),deck.pop()]
    if hand_value(player)==21: return 1.5 if hand_value(dealer)!=21 else 0
    while True:
        action=basic_strategy(player,dealer[0])
        if action=="stand": break
        if action in ("hit","double"): player.append(deck.pop())
        if hand_value(player)>21: return -1
        if action=="double": break
    while hand_value(dealer)<17: dealer.append(deck.pop())
    pv,dv=hand_value(player),hand_value(dealer)
    if dv>21: return 1
    return 1 if pv>dv else (-1 if pv<dv else 0)
if __name__=="__main__":
    random.seed(42);deck=new_deck();wins=draws=losses=0
    for _ in range(10000):
        r=play_hand(deck)
        if r>0: wins+=1
        elif r<0: losses+=1
        else: draws+=1
    print(f"10K hands: W={wins} D={draws} L={losses}")
    print(f"House edge: {(losses-wins)/10000*100:.2f}%")
    print("Blackjack OK")
