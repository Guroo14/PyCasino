from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from blackjack import BlackjackWindow
import sys, random

class Blackjack(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = BlackjackWindow()
        self.ui.setupUi(self)

        self.balance = 1000
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.split_hand = []
        self.playing_split = False
        self.current_hand = []

        self.card_images = self.build_card_image_dict()

        self.ui.hitButton.clicked.connect(self.hit)
        self.ui.standButton.clicked.connect(self.stand)
        self.ui.newGameButton.clicked.connect(self.new_game)
        self.ui.splitButton.clicked.connect(self.split)
        self.ui.pushButton_6.clicked.connect(self.to_bacc)

        self.new_game()

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
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.split_hand = []
        self.playing_split = False
        self.current_hand = self.player_hand
        self.ui.resultLabel.setText("")
        self.lock_buttons(False)
        self.ui.newGameButton.setEnabled(False)  # disable until round ends
        self.update_ui(hide_dealer=True)
        self.check_split_option()
        self.ui.newGameButton.setEnabled(False)

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']
        return [r + s for r in ranks for s in suits]

    def card_value(self, card):
        rank = card[:-1]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)

    def hand_value(self, hand):
        value = sum(self.card_value(c) for c in hand)
        aces = sum(1 for c in hand if c[:-1] == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def update_ui(self, hide_dealer=False):
        # Player cards
        for i in range(5):
            label = getattr(self.ui, f'playerCard{i+1}', None)
            if label:
                if i < len(self.player_hand):
                    self.show_card(label, self.player_hand[i])
                else:
                    label.clear()

        # Split cards
        for i in range(5):
            label = getattr(self.ui, f'splittedCard{i+1}', None)
            if label:
                if i < len(self.split_hand):
                    self.show_card(label, self.split_hand[i])
                else:
                    label.clear()

        # Dealer cards
        for i in range(5):
            label = getattr(self.ui, f'dealerCard{i+1}', None)
            if label:
                if i < len(self.dealer_hand):
                    if i == 0 or not hide_dealer:
                        self.show_card(label, self.dealer_hand[i])
                    else:
                        self.show_card(label, "🂠")  # Optionally use a back image
                        label.setPixmap(QPixmap("Deck/background.jpg"))
                        label.setScaledContents(True)
                else:
                    label.clear()

        self.ui.balanceLabel.setText(f"Balance: ${self.balance}")

    def lock_buttons(self, lock):
        self.ui.hitButton.setEnabled(not lock)
        self.ui.standButton.setEnabled(not lock)
        self.ui.splitButton.setEnabled(not lock)

    def check_split_option(self):
        if len(self.player_hand) == 2 and self.player_hand[0][:-1] == self.player_hand[1][:-1] and self.balance >= 100:
            self.ui.splitButton.setEnabled(True)
        else:
            self.ui.splitButton.setEnabled(False)

    def hit(self):
        if not self.deck:
            self.ui.resultLabel.setText("Deck is empty!")
            return

        self.current_hand.append(self.deck.pop())
        self.update_ui(hide_dealer=True)

        if self.hand_value(self.current_hand) > 21:
            if self.playing_split and self.current_hand == self.player_hand:
                self.ui.resultLabel.setText("First hand busts.")
                self.current_hand = self.split_hand
            elif self.playing_split:
                self.end_split_round()
            else:
                self.end_round("Bust! Dealer wins.")

        if self.playing_split and self.current_hand[0][:-1] == 'A' and len(self.current_hand) == 2:
            self.stand()

    def stand(self):
        if self.playing_split and self.current_hand == self.player_hand:
            self.current_hand = self.split_hand
            self.update_ui(hide_dealer=True)
        elif self.playing_split:
            self.end_split_round()
        else:
            self.dealer_ai()
            self.evaluate_winner()

    def split(self):
        if len(self.player_hand) == 2 and self.player_hand[0][:-1] == self.player_hand[1][:-1]:
            self.split_hand = [self.player_hand.pop()]
            self.split_hand.append(self.deck.pop())
            self.player_hand.append(self.deck.pop())
            self.playing_split = True
            self.current_hand = self.player_hand
            self.balance -= 100
            self.update_ui(hide_dealer=True)
            self.ui.splitButton.setEnabled(False)
            self.ui.newGameButton.setEnabled(False)

    def dealer_ai(self):
        while self.hand_value(self.dealer_hand) < 17:
            if not self.deck:
                self.ui.resultLabel.setText("Deck is empty!")
                return
            self.dealer_hand.append(self.deck.pop())
        self.update_ui(hide_dealer=False)

    def evaluate_winner(self):
        player_total = self.hand_value(self.player_hand)
        dealer_total = self.hand_value(self.dealer_hand)

        if dealer_total > 21:
            self.balance += 100
            self.ui.resultLabel.setText("Dealer Busts! You Win.")
        elif player_total > dealer_total:
            self.balance += 100
            self.ui.resultLabel.setText("You Win!")
        elif player_total < dealer_total:
            self.balance -= 100
            self.ui.resultLabel.setText("You Lose.")
        else:
            self.ui.resultLabel.setText("Push. It's a tie.")

        self.check_game_over()
        self.lock_buttons(True)
        self.update_ui(hide_dealer=False)
        self.ui.newGameButton.setEnabled(True)

    def end_round(self, result_text):
        self.balance -= 100
        self.ui.resultLabel.setText(result_text)
        self.lock_buttons(True)
        self.update_ui(hide_dealer=False)
        self.check_game_over()

        self.ui.newGameButton.setEnabled(True)

    def end_split_round(self):
        self.dealer_ai()
        total_win = 0

        for hand in [self.player_hand, self.split_hand]:
            player_total = self.hand_value(hand)
            dealer_total = self.hand_value(self.dealer_hand)

            if player_total > 21:
                result = "Bust!"
            elif dealer_total > 21 or player_total > dealer_total:
                result = "Win"
                total_win += 100
            elif player_total < dealer_total:
                result = "Lose"
                total_win -= 100
            else:
                result = "Push"

            self.ui.resultLabel.setText(self.ui.resultLabel.text() + f"\nHand: {result}")

        self.balance += total_win
        self.lock_buttons(True)
        self.update_ui(hide_dealer=False)
        self.check_game_over()
        self.ui.newGameButton.setEnabled(True)

    def check_game_over(self):
        if self.balance <= 0:
            self.ui.resultLabel.setText(self.ui.resultLabel.text() + "\nGame Over!")
            self.lock_buttons(True)
    def to_bacc(self):
        from baccarat_logic import Baccarat
        self.baccarat_window = Baccarat()
        self.baccarat_window.show()
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Blackjack()
    window.show()
    sys.exit(app.exec_())