"""카드 게임"""

class Card:
    "카드와 그 카드의 이미지 파일명을 표현하는 Card 클래스"
    FACES = ['Ace', '2','3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Joker']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades', 'Black', 'Color']

    def __init__(self, face, suit):
        """페이스와 스위트로 Card 객체 초기화"""
        self._face = face
        self._suit = suit
    
    @property
    def face(self):
        """카드의 face를 반환한다."""
        return self._face
    
    @property
    def suit(self):
        """카드의 suit을 반환한다."""
        return self._suit

    @property
    def image_name(self):
        """카드의 이미지 파일명을 반환한다."""
        return str(self).replace(' ', '_') + '.png'

    def __repr__(self):
        """repr() 함수에 사용될 문자열 반환"""
        return f"Card(face='{self.face}', suit='{self.suit}')"
    
    def __str__(self):
        """str() 함수에 사용될 문자열 반환"""
        return f'{self.face} of {self.suit}'
    
    def __format__(self, format):
        """서식이 적용된 문자열을 반환"""
        return f'{str(self):{format}}'
