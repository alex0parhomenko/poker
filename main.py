from pypokerengine.api.game import setup_config, start_poker

from pypokerengine.api.game import setup_config, start_poker

from nn import Net
from nn_player import NNPlayer


def main() -> int:
    net = Net()
    config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
    config.register_player(name="p1", algorithm=NNPlayer(net))
    config.register_player(name="p2", algorithm=NNPlayer(net))
    game_result = start_poker(config, verbose=1)
    print(game_result)
    return 0


if __name__ == '__main__':
    main()
