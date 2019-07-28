
class StateAndReward:
    def __init__(self):
        pass

    def state(state):
        return tuple(state.get())

    def reward(state):
        if state.latest_result == 1 or state.latest_result == 2:
            return state.ticks
        if state.latest_result == 0:
            return 0