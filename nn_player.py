import torch
from pypokerengine.engine.card import Card
from pypokerengine.players import BasePokerPlayer
from torch import Tensor

from nn import Net


class NNPlayer(BasePokerPlayer):
    def __init__(self, net: Net):
        super().__init__()
        self.__net = net
        self.__input_dimension = [56]

    def declare_action(self, valid_actions, hole_card, round_state):
        board = [*hole_card, *round_state['community_card']]
        street = round_state['street']
        input_tensor = self.__create_input_by_board_and_street(board, street)
        # Probability of Fold/Call/Raise
        probabilities = self.__net(input_tensor)
        _, action, amount = self.__get_most_likely_action(valid_actions, probabilities)
        return action, amount

    def __get_most_likely_action(self, valid_actions, probabilities):
        probability_to_action = []
        for action in valid_actions:
            if action['action'] == 'fold':
                probability_to_action.append([probabilities[0].item(), 'fold', action["amount"]])
            elif action['action'] == 'call':
                probability_to_action.append([probabilities[1].item(), 'call', action["amount"]])
            elif action['action'] == 'raise':
                probability_to_action.append([probabilities[2].item(), 'raise', action["amount"]['max']])
        return list(sorted(probability_to_action, key=lambda x: x[0]))[-1]

    def __create_input_by_board_and_street(self, board, street) -> Tensor:
        t = torch.zeros(self.__input_dimension)
        t[self.__encode_street(street)] = 1
        for card in board:
            t[Card.from_str(card).to_id()] = 1
        return t

    def __encode_street(self, street: str) -> int:
        if street == 'preflop':
            return 0
        elif street == 'flop':
            return 1
        elif street == 'turn':
            return 2
        elif street == 'river':
            return 3
        raise Exception("Unknown street")

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
