from card import Card
import random

class Deck:
    """덱을 구성하는 클래스"""
    NUMBER_OF_CARDS = 54 # 카드 상수 초기화

    def __init__(self, *player):
        """원카드 클래스 초기화"""
        self.board_num = 0 # 게임 중 보드에 놓여있는 카드의 수
        self.deck_num = 54 # 게임 중 덱에 남아있는 카드의 수
        self.deck = [(face, suit) for face in Card.FACES[:-1] for suit in Card.SUITS[:-2]] + [('Joker', 'Black'), ('Joker','Color')] # 카드의 덱 초기화
        self.player = player # 게임에 참여하는 플레이어 이름
        self.player_num = len(self.player) # 게임에 참여하는 플레이어 수
        self.shuffle
        self.player_setting = self.give_out_card
        self.board = self.init_setting

    def draw_card(self, cnt):
        """card_role에서 적용된 규칙에 따라 드로우 하는 수를 입력받아 카드 드로우 진행"""
        self.cnt = cnt # rule에 적용되는 드로우 개수
        
        # 드로우 해야하는 카드의 수가 덱의 수보다 같거나 작은 경우
        if self.deck_num >= self.cnt:
            draw_list = [self.deck.pop() for _ in range(cnt)]
            return draw_list
        
        # 드로우 해야하는 카드의 수가 덱의 수보다 많은 경우
        else:
            residual_cnt = self.cnt - self.deck_num # 잔차 = 드로우 해야하는 수 - 남아 있는 덱의 수
            draw_list = [self.deck.pop() for _ in range(self.deck_num)] # 덱에 있는 모든 카드 드로우
            self.reshuffle # 덱 리셔플 함수 호출
            
            # 남은 잔차 덱 드로우
            for _ in range(residual_cnt):
                draw_list.append(self.deck.pop())
            return draw_list   

    def __str__(self):
        """현재 덱에 있는 리스트를 반환"""
        s = ''

        for index, card in enumerate(self.deck):
            s += f'{card[0]:>5} of {card[1]:<10}'
            if (index + 1) % 4 == 0:
                s += '\n'
        return s        

    @property
    def init_setting(self):
        """원카드 게임을 시작할 때 처음 보드에 놓이는 시작 카드 설정"""
        self.board = self.deck.pop() # 덱 위에 있는 카드 뽑기
        self.deck_num -= 1 # 덱에 남아 있는 카드 1개 제거
        self.board_num += 1 # 보드에 놓여있는 카드 수 1개 증가
        print(f'현재 보드 : {self.board}')
        return self.board

    @property
    def shuffle(self):
        """카드를 섞는 함수"""
        return random.shuffle(self.deck)

    @property
    def give_out_card(self):
        """플레이어 수에 따라 카드 7개씩 분배"""
        setting ={ name:{} for name in self.player}

        for k in setting.keys():
            draw_list = [self.deck.pop() for _ in range(7)]
            self.deck_num -= len(draw_list)
            setting[k] = draw_list

        return setting

    @property
    def reshuffle(self):
        """덱에 있는 카드의 개수가 0이 될 경우 보드에 있는 카드를 섞어서 덱으로 만드는 함수"""
        self.deck_num = self.board_num
        self.board_num = 0
        self.deck = self.board
        self.borad = None
        self.shuffle
        #return self.deck_num, self.board_num, self.deck, self.borad

    @property
    def check_deck(self):
        """덱에 있는 카드가 0개가 되는지 체크하는 함수"""
        if self.deck <= 0:
            return self.reshuffle
