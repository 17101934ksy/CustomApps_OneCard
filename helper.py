from player import Player

def link_player(deck):
    # 덱과 플레이어를 연결해주는 함수
    player_list = []
    for k,v in deck.player_setting.items():
        player = Player(k,v)
        player_list.append(player)
    return player_list