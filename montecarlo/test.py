from ai import AI
from game_env_interface import Game
import argparse

def init_game(size, ships, samples):
    # Build the AI boards and init the AI
    ai_env = Game(size, ships)
    computer = AI(ai_env, samples)
    computer.eval_model(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', help='The size of the board, default: 10', default=10)
    parser.add_argument('--ship_sizes', help='Array of ship sizes to randomly place, default: "5,4,3,3,2"', default='5,4,3,3,2')
    parser.add_argument('--monte_carlo_samples', help='The number of samples to get the algorithm to do, default: 10000', default=10000)

    args = parser.parse_args()

 
    print("Chosen args: ", args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples)
    init_game(args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples)
 
