class Player:

    """게임을 진행하는 플레이어 정의 클래스"""
    def __init__(self, name, card_list):
        self.name = name
        self.card_list = card_list

    def update_card_list(self,card_rule):
        self.card_list = card_rule.released_card(self.card_list)