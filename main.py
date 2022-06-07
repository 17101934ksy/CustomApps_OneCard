"""
원카드 게임

- 게임 개발 설명
    1. 개발자 
        서울과학기술대학교 산업정보시스템공학과, ICT인공지능전공 : 고세윤

    2. 게임 목적 
        트럼프 카드로 하는 원카드 게임구현.

- 게임 방법:
    1. 게임 진행 방법
        플레이어와 컴퓨터는 1:1로 원카드 게임을 진행한다.
        플레이어와 컴퓨터는 랜덤으로 선공이 정해지며, 게임 규칙에 따라 진행된다.
        게임 규칙은 2번 항목에 세부적으로 기술해 놓았으며
        먼저 카드를 0개로 만드는 플레이어가 승리한다.
    
    2. 게임 규칙
        원카드는 54장의 카드로 구성된다.
        FACE 와 SUIT는 숫자(특성)와 무늬를 나타낸다.

        FACE : ACE, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King
        SUIT : Spades, Clubs, Hearts, Diamonds
        Joker : Black_Joker, Color_Joker

        FACE * SUIT = 52장
        Joker = 2장 

        플레이어와 컴퓨터는 시작하면 7장씩 랜덤하게 드로우를 진행한다.
        초기 카드가 보드에 한잘 놓여지며 게임이 시작된다.

        선공 플레이어는 보드에 놓여진 카드와 같은 무늬 or 같은 숫자 혹은 조커를 보드에 낼 수 있다.
        후공 플레이어는 가장 최근 보드에 놓여진 카드에 선공 플레이어가 진행한 방법과 동일하게 카드를 낸다.
        만약 보드에 놓여진 카드와 같은 무늬가 없거나 같은 숫자 혹은 조커가 없을 경우, 카드를 한장 드로우 한다.
        
        카드에는 특성이 존재하는 카드가 있다. 카드 특성은 3번 항목에 자세하게 기술하였다. 
        카드 중에는 공격카드가 있는데, 공격을 받았을 시에는 카드를 해당하는 규칙만큼 카드를 드로우 해야한다.
        만약 공격을 받았을 때, 우선순위가 높은 카드가 있다면 공격을 방어할 수 있으며, 
        공격 방어시 드로우 해야하는 카드 수는 누적되어 방어를 못한 플레이어가 누적 카드를 모두 드로우 한다. 
        
        순서는 번갈아 진행하며 먼저 카드를 0개로 만든 플레이어가 승리한다.

    3. 카드 특성
        ACE : 공격카드로 공격을 받는 상대방은 3장의 카드를 드로우 해야한다.
        
        Spade_ACE : ACE 중 스페이드 A는 특수 카드로 공격 받은 상대방은 5장의 카드를 드로우 해야한다. 
                    또한, 흑백 조커의 공격을 받았을 시 방어카드로 사용할 수 있다.

        2 : 공격 카드로 공격을 받는 상대방은 2장의 카드를 드로우 해야한다
        
        7 : 행운의 카드로 보드 위에 놓여진 무늬와 상관없이 플레이어는 원하는 무늬로 바꿀 수 있다.
        
        Jack : 플레이어는 해당 진행 방향에서 다음 순서 플레이어를 점프하여 게임을 진행한다.
                2인 플레이시에는 다시 순서가 자신에게 오도록 사용 가능하다.  
        Queen : 플레이어는 해당 순서를 역방향으로 바꾼다. 2인이서 진행할 경우에는 순서의 방향이 의미가 없다.

        King : 플레이어는 K와 함께 같은 무늬 카드를 동시에 낼 수 있다.

        Black_Joker : 흑백 조커는 공격 카드로 공격 받는 대상은 7장을 드로우 해야한다.
                      이때 흑백 조커가 낼 수 있는 무늬는 흑백에 해당한다. (스페이드, 클로버)
                      해당 카드는 스페이드 A 로 방어할 수 있다.
        
        Color_Joker : 컬러 조커는 공격 카드로 공격 받는 대상은 10장을 드로우 해야한다.
                      컬러 조커는 무늬에 상관없이 모두 낼 수 있다.
                      해당 카드는 방어할 수 없다.

"""

import random
from decks import Deck
from player import Player
from card_rule import Rule, Card_Rule
from helper import link_player

# 게임에 참여할 플레이어
player_name1 = input("게임에 참여할 플레이어1의 이름을 입력하세요. :    ")
player_name2 = input("게임에 참여할 플레이어2의 이름을 입력하세요. :    ")
print()

first_sequence = random.random()>0.5

deck = Deck(player_name1, player_name2)
card_rule = Card_Rule(deck)

if first_sequence:
    player1 = Player(player_name1, deck.player_setting[player_name1])
    player2 = Player(player_name2, deck.player_setting[player_name2])
else:
    player1 = Player(player_name2, deck.player_setting[player_name2])
    player2 = Player(player_name1, deck.player_setting[player_name1])


game_end = False
while not game_end :
    if len(player1.card_list) == 0 or len(player2.card_list) == 0:
        game_end == True
        break
    print('\n')
    print(f'{player1.name}의 차례입니다.')
    card_rule.turn = True
    player1.update_card_list(card_rule=card_rule)

    print('\n')
    print(f'{player2.name}의 차례입니다.')
    card_rule.turn = True
    player2.update_card_list(card_rule=card_rule)

if len(player1.card_list) == 0:
    print(f'{player1.name}이 승리하였습니다.')
elif len(player2.card_list) == 0:
    print(f'{player2.name}이 승리하였습니다.')
