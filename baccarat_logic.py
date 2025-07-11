from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import sys, random
from baccarat import BaccaratWindow


class Baccarat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = BaccaratWindow()
        self.ui.setupUi(self)

        self.balance = 1000
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        self.card_images = self.build_card_image_dict()

        self.ui.playerButton.clicked.connect(self.player_bet)
        self.ui.dealerButton.clicked.connect(self.dealer_bet)
        self.ui.tieButton.clicked.connect(self.tie_bet)
        self.ui.newGameButton.clicked.connect(self.new_game)
        self.ui.pushButton_5.clicked.connect(self.to_bj)
        self.new_game()
    def to_bj(self):
        from Blackjack_logic import Blackjack
        self.blackjack_window = Blackjack()
        self.blackjack_window.show()
        self.close()

    def build_card_image_dict(self):
        rank_map = {
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9', '10': '10',
            'J': 'jack', 'Q': 'queen', 'K': 'king', 'A': 'ace'
        }
        suit_map = {
            '♠': 'spades',
            '♥': 'hearts',
            '♦': 'diamonds',
            '♣': 'clubs'
        }

        card_images = {}
        for rank_code, rank_name in rank_map.items():
            for suit_code, suit_name in suit_map.items():
                card_code = f"{rank_code}{suit_code}"
                image_path = f"Deck/{rank_name}_of_{suit_name}.jpg"
                card_images[card_code] = image_path
        return card_images

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']
        return [r + s for r in ranks for s in suits]

    def card_value(self, card):
        rank = card[:-1]
        if rank in ['10', 'J', 'Q', 'K']:
            return 0
        elif rank == 'A':
            return 1
        else:
            return int(rank)

    def hand_value(self, hand):
        value = sum(self.card_value(c) for c in hand) % 10
        return value

    def show_card(self, label, card_code):
        path = self.card_images.get(card_code)
        if path:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                label.setPixmap(pixmap)
                label.setScaledContents(True)
                return
        label.clear()

    def new_game(self):
        if self.balance <= 0:
            self.ui.resultLabel.setText("You are out of money. Game over!")
            self.ui.newGameButton.setEnabled(False)
            return

        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.ui.resultLabel.setText("")
        self.lock_buttons(False)
        self.ui.newGameButton.setEnabled(False)

        self.update_ui()

    def player_bet(self):
        self.play_round('player')

    def dealer_bet(self):
        self.play_round('dealer')

    def tie_bet(self):
        self.play_round('tie')

    def play_round(self, bet_on):
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        player_value = self.hand_value(self.player_hand)
        dealer_value = self.hand_value(self.dealer_hand)

        if player_value <= 5:
            self.player_hand.append(self.deck.pop())
            player_value = self.hand_value(self.player_hand)

        if dealer_value <= 5:
            self.dealer_hand.append(self.deck.pop())
            dealer_value = self.hand_value(self.dealer_hand)

        self.update_ui()

        result = ''
        if player_value > dealer_value:
            result = 'player'
        elif dealer_value > player_value:
            result = 'dealer'
        else:
            result = 'tie'

        if bet_on == result:
            if result == 'tie':
                self.balance += 800
                self.ui.resultLabel.setText("Tie! You win 8x your bet!")
            else:
                self.balance += 100
                self.ui.resultLabel.setText(f"You bet on {bet_on}. You Win!")
        else:
            self.balance -= 100
            self.ui.resultLabel.setText(f"You bet on {bet_on}. You Lose.")

        self.lock_buttons(True)
        self.ui.newGameButton.setEnabled(True)
        self.ui.balanceLabel.setText(f"Balance: ${self.balance}")
        self.check_game_over()

    def update_ui(self):
        for i in range(5):
            label = getattr(self.ui, f'playerCard{i+1}', None)
            if label:
                if i < len(self.player_hand):
                    self.show_card(label, self.player_hand[i])
                else:
                    label.clear()

        for i in range(5):
            label = getattr(self.ui, f'dealerCard{i+1}', None)
            if label:
                if i < len(self.dealer_hand):
                    self.show_card(label, self.dealer_hand[i])
                else:
                    label.clear()

        self.ui.balanceLabel.setText(f"Balance: ${self.balance}")

    def lock_buttons(self, lock):
        self.ui.playerButton.setEnabled(not lock)
        self.ui.dealerButton.setEnabled(not lock)
        self.ui.tieButton.setEnabled(not lock)

    def check_game_over(self):
        if self.balance <= 0:
            self.ui.resultLabel.setText(self.ui.resultLabel.text() + "\nGame Over!")
            self.lock_buttons(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Baccarat()
    window.show()
    sys.exit(app.exec_())