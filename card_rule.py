# 원카드의 룰을 정의하는 클래스
from decks import Deck

class Rule:
    """ 
    룰을 적용하는 클래스
    1.
    다음 상수는 주석의 설명에 따라 드로우 하는 카드의 수를 나타낸다.
    
    ONE :        자신의 카드를 모두 소진하지 않았을 때, 자신의 턴 때 낼 수 있는 카드가 없을 경우, 혹은 카드의 규칙에 어긋나는 카드를 냈을 경우
    TWO :        2의 공격을 받았을 경우
    THREE :      스페이드a를 제외하여 공격을 받았을 경우
    FIVE :       스페이드a의 공격을 받았을 경우
    SEVEN :      블랙 조커의 공격을 받았을 경우
    TEN :        컬러 조커의 공격을 받았을 경우
    
    2.
    다음 딕셔너리 상수는 SUIT의 우선 순위와 FACE의 파워를 나타낸다.
    카드의 파워가 높을수록 더 카드의 강한 영향력을 갖는다.

    FACES의 파워 :
    Joker > Ace > 2 > 알파벳 카드 >= 일반 숫자

    SUITS의 파워 :
    컬러 > 흑백 > 스페이드 > 나머지 무늬

    """
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    SEVEN = 7
    TEN = 10

    FACES_POWER = {
        'Ace' : 3, '2' : 2, '3' : 1, '4' : 1, 
        '5' : 1, '6' : 1, '7' : 1, '8' : 1,
        '9' : 1, '10' : 1, 'Jack' : 1, 'Queen': 1,
        'King' : 1, 'Joker': 4
    }

    SUITS_POWER = {
        'Color' : 4, 'Black' : 3, 'Spade' : 2, 'Hearts' : 1,
        'Diamonds': 1, 'Clubs' : 1, 'Spades': 1
        }


class Card_Rule(Rule):
    """카드를 내는 규칙을 정의하는 클래스"""
    def __init__(self, decks):
        self.turn = False # 자신의 turn이 True일 때 카드를 내도록 turn -> False 초기화 

        self.decks = decks # 덱 정의

        self.board = decks.board # 보드에 놓여진 카드 초기화(카드 게임 시작시 처음 나오는 카드로 초기화)
        self.board_faces, self.board_suits = self.board
        self.board_valid = False # 보드에 놓여진 카드가 현재 시점에 유효한 공격인지 판단
        
        self.card = None # 이번에 내려는 카드
        self.card_faces = None # 이번에 낸 카드의 faces 정의
        self.card_suits = None #  이번에 낸 카드의 suits 정의
        
        self.want_suits = None # 7로 인한 변경카드 초기화

        self.draw_penalty = 0 # 규칙에 어긋나느 카드를 냈을 때 드로우 해야하는 카드
        self.draw_attack = 0 # 드로우 카드 0 설정

# 수정
    def released_card(self, card_list):
        """보드위에 놓여진 카드를 저장하는 함수"""

        print("현재 소지 중인 카드")
        for j, card in enumerate(card_list):
            print(f'{j+1:<3} {card}')
        
        card_num = [0]

        # 입력이 -1로 끝나고, 중복되지 않아야 함. card_index가 card_list의 부분 집합이어야 함
        while not ((card_num[-1] == -1) and (len((card_num))==len(set(card_num))) and (set(card_num) <= set(range(1, len(card_list) + 1)) | {-1})) :
            try:
                card_num = list(map(int, input("내고 싶은 카드를 순서대로 입력하세요.(스페이스로바로 구분) 입력 종료시 -1 입력: ").split())) # 리스트 형태 [0,1,2,-1]
            except:
                print("잘못 입력하였습니다. 다시 입력해주세요 \n")
        
        self.rule_king_jack(card_list=card_list)
        turn_cnt = 0  # 카드를 1번 내는 것은 유효하나, 아예 내지 않을 경우 패널티 적용, 두번째 부터는 self.turn = True 일 때만 가능 하므로 검증하는 변수
        card_value_list = [card_list[i-1] for i in card_num if i != -1]
        print(f'card_list_value : {card_value_list}')

        for j_index, index in enumerate(card_num): 
            
            print(f'플레이어가 낸 횟수 : {turn_cnt}')

            if (turn_cnt == 0) and (index-1 == -2):
                self.rule_turn_zero(card_list)
                break
            elif (turn_cnt != 0) and (index-1 == -2):
                print('턴을 종료합니다.')
                break

            turn_cnt += 1 # 내려고 하는 카드의 순번이 유효하면 턴 횟수 1 증가
            tmp_penalty = self.draw_penalty # 패널티 카드를 받을경우 턴을 종료하기 위한 체크 변수 할당 
            
            self.card = card_list[index-1] # 자신의 턴이 유효한지 판단하기 위해 card의 faces와 suits를 복사
            self.card_faces, self.card_suits = self.card

            if turn_cnt > 1:
                self.turn = self.rule_same # 자신의 턴이 유효한지 판단

                if not self.turn:
                    print('debug ********** turn 검증 : False')
                    self.rule_penalty(card_list)
                    print(f'패널티 카드를 받아 턴을 종료합니다. : code1')
                    break
                else:
                    print('debug ********** turn 검증 : True')
                    if not self.rule_valid(tmp_penalty, card_list, card_value_list, j_index):
                        break

            elif turn_cnt == 1:
                if not self.rule_valid(tmp_penalty, card_list, card_value_list, j_index):
                    break

            print(f'보드에 놓은 카드 : {self.board}')
            self.turn = False
        
        print(f'보드 : {self.board}\n보드 faces : {self.board_faces}\n보드 suits : {self.board_suits}')
        print(f'카드 faces : {self.card_faces}\n카드 suits : {self.card_suits}\n카드 리스트 개수 : {len(card_list)}')
        return card_list
    
    def rule_valid(self, tmp_penalty, card_list, card_value_list, j_index):
        """ 내려고 하는 카드의 적합성을 검정하는 함수"""

        print(f'\n{self.card_faces} {self.card_suits} 를 냅니다\n')  
        self.release_card(card_list)  # 내려고 하는 카드의 적합성 검정
        if tmp_penalty != self.draw_penalty:
            print('debug ********** turn 검증 : True, 패널티 : O')
            return False
        else:
            self.rule_deck(card_list=card_list, card_value_list=card_value_list, card_cnt=j_index)

    def release_card(self, card_list):
        """낸 카드의 적합성을 검정하고 특성에 맞는 다른 함수를 호출하는 함수"""

        if self.board_valid:
            print("debug ************** 디버그1")
            if self.card_faces == 'Joker':
                self.check_joker(card_list=card_list)
                print("debug ************** 디버그2")

            elif self.board_suits == self.card_suits: # 조커가 아닌 카드일 경우 suits이 같아야함
                print("debug ************** 디버그3")
                self.check_special if (self.FACES_POWER[self.board_faces]  <= self.FACES_POWER[self.card_faces]) else self.rule_penalty(card_list)

            else: # 조커가 아니고 같은 suits이 아닐 경우
                if self.board_faces == self.card_faces: # 같은 faces 경우 낼 수 있음
                    print("debug ************** 디버그4")
                    if self.board == ('Ace','Spades'): # 보드에 있는 카드가 Ace, Spades 라면 일반 Ace로 막을 수 없음 
                        print("debug ************** 디버그5")                           
                        self.rule_penalty(card_list) if self.card_faces == 'Ace' else self.help_pass
                    else:
                        print("debug ************** 디버그6")
                        self.check_special

                else: # 규칙에 어긋날 경우 패널티 적용
                    print("debug ************** 디버그7")
                    self.rule_penalty(card_list)
        else:
            if (self.board_suits == self.card_suits) or (self.board_faces == self.card_faces) \
                or (self.board_suits == 'Black' and self.card_suits in ['Spades','Clubs','Color']) or \
                    (self.board_suits == 'Color'):
                print("debug ************** 디버그8")
                self.check_joker(card_list=card_list)
                self.check_special
            else:
                print("debug ************** 디버그9")
                self.rule_penalty(card_list)

    def check_joker(self, card_list):
        """조커 카드를 판단하여 해당 함수 호출"""
        
        # 보드 위 카드가 영향력이 있을 때, 흑백 조커는 스페이드와 클로버에만 가능 / 보드 위 카드가 영향력이 없을 때, 스페이드 클로버 컬러에 흑백 조커 가능
        if self.card_suits == 'Black':
            (self.rule_black if self.board_suits in ['Spades', 'Clubs'] else self.rule_penalty(card_list)) if self.board_valid else \
                (self.rule_black if self.board_suits in ['Spades', 'Clubs', 'Color'] else self.rule_penalty(card_list))

        # 컬러조커는 모든카드에 적용
        elif self.card_suits == 'Color':
            self.rule_color


    def rule_penalty(self, card_list):
        """어긋나는 카드를 냈을 시 모든 카드를 드로우 하는 함수"""

        print('잘못된 카드를 내서 패널티 카드를 받습니다.')
        self.draw_penalty += self.ONE
        self.turn = False
        card_list.extend(self.decks.draw_card(self.draw_attack + self.draw_penalty))
        self.rule_draw_init

        # 잔여 카드 모드 드로우

    def rule_turn_zero_penalty(self, card_list):
        """카드를 내지 않고 종료했을 시에 받는 패널티 정의 함수"""
        self.turn = False
        if self.draw_attack > 0:
            card_list.extend(self.decks.draw_card(self.draw_attack))
            print('카드를 내지 않아 누적된 카드를 받습니다. : code5 ')
        
        elif self.draw_attack == 0:
            self.draw_penalty += self.ONE
            card_list.extend(self.decks.draw_card(self.draw_penalty))
            print('카드를 내지 않아 패널티 카드를 받습니다. : code6 ')
        else:
            raise ValueError('error')
        self.rule_draw_init # 잔여카드 모두 드로우 후 드로우 해야하는 양 리셋
  
    def rule_draw_attack(self, num):
        print(f'{self.card_faces} of {self.card_suits} 공격')
        self.draw_attack += num        

    def rule_king_jack(self, card_list):
        """king 이나 jack을 뽑았을 경우"""
        for i in range(0, len(card_list)):
            if (card_list[i] in ['King', 'Jack']) and (card_list[i+1] == -1):
                self.rule_turn_zero(card_list=card_list)

    def rule_deck(self, card_list, card_value_list ,card_cnt):
        """새로운 보드를 만드는 호출 함수"""

        self.card = card_list.pop(card_list.index(card_value_list[card_cnt]))
        self.card_faces, self.card_suits = self.card # 내려고 하는 카드 faces, suits 재정의

        self.rule_new_board if self.want_suits != None else self.rule_board
        self.rule_valid_True

    def rule_turn_zero(self, card_list):
        """자신의 턴 때 카드를 내지 않고 종료한 경우"""
        self.card = (None, None)
        self.card_faces, self.card_suits = self.card
        self.rule_turn_zero_penalty(card_list)

    @property
    def check_special(self):
        """face가 스페셜한 특성이 있는 카드를 냈는지 파악하여 함수 호출"""      
        # 카드의 face의 숫자에 따라 다른 함수 호출

        self.rule_acetwo if self.card_faces in ['Ace', '2'] else self.rule_seven if self.card_faces =='7' else self.help_pass

    @property
    def rule_acetwo(self):
        """ 공격에 따른 드로우 개수 설정 함수 """
        if self.card_faces == 'Ace':
            if self.card_suits == 'Spades':
                self.rule_draw_attack(self.FIVE)
    
            elif self.card_suits in ['Hearts, Diamonds, Clubs']:
                self.rule_draw_attack(self.THREE)

        elif self.card_faces == '2':
            self.rule_draw_attack(self.TWO)
    
    @property
    def rule_color(self):
        print(f'Color of Joker 공격')
        self.draw_attack += 10

    @property
    def rule_black(self):
        print(f'Black of Joker 공격')
        self.draw_attack += 7

    @property
    def rule_seven(self):
        """face가 7인 경우 원하는 suit으로 바꿔주는 함수"""
        # 초기 입력
        self.want_suits = input('Hearts, Spades, Clubs, Diamonds 중에서 하나를 입력하세요: ').capitalize()

        # 입력 받은 값 검증 시행
        while self.want_suits not in ['Hearts', 'Spades', 'Clubs', 'Diamonds']:
            self.want_suits = input('입력이 잘못되었습니다. Hearts, Spades, Clubs, Diamonds 중에서 하나를 입력하세요: ').capitalize()
        # 입력 받은 무늬로 보드를 변경
        print(f'플레이어가 무늬를 {self.want_suits} 으로 바꿨습니다.')

    @property
    def rule_same(self):
        """무늬는 다르지만 같은 face가 존재할 시 혹은 King or jack을 냈을 시 같은 턴 안에 카드를 낼 수 있음"""
        if not self.turn:
            self.turn = True if (self.board_faces == self.card_faces) or (self.board_faces in ['King', 'Jack']) else False
        return self.turn

    @property
    def rule_new_board(self):
        """7로 인해 자신이 낸 카드의 faces와 새로운 보드 suits를 만드는 함수"""
        
        self.board_faces, self.board_suits = self.card_faces, self.want_suits # 낸 카드의 숫자와, 새로 정의한 suits로 board 초기화
        self.board = (self.board_faces, self.board_suits) # 최종 보드 이미지 패킹 
        self.card_suits = self.want_suits

    @property
    def rule_board(self):
        """자신이 낸 카드로 보드를 새롭게 바꿔주는 함수"""
        self.board = self.card
        self.board_faces, self.board_suits = self.board # board 언패킹

    @property
    def rule_draw_init(self):
        """공격을 받거나 패널티 카드를 받을 경우 드로우 카드 초기화"""
        self.draw_penalty = self.draw_attack = 0
        self.board_valid = False

    @property
    def rule_valid_False(self):
        """시작할 때 혹은 드로우를 마쳤을 경우 카드 패널티가 적용되지 않도록 하는 함수"""
        self.board_valid = False
    
    @property
    def rule_valid_True(self):
        """패널티가 적용되는 보드 함수"""
        self.board_valid = True

    @property
    def help_pass(self):
        pass



    ## 디버그 valid가 false가 되면 else문으로 넘어가는데 내는카드가 조커일경우 디버그 9로 
    ## 오류가 남 즉 else if문에 if문에 board 조건 말고 내는 카드의 조건도 추가로 넣어줘야함