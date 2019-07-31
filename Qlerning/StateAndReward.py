
class StateAndReward:
    def __init__(self):
        pass

    def state(self, state):
        return tuple(state.get())

    def reward(self, state):
        if state.latest_result == 1 or state.latest_result == 2:
            return state.ticks
        if state.latest_result == 0:
            return 0