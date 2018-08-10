
def State_init(self, director):
    self.d = director


State = type('State', (), {'__init__': State_init})


class FSM:
    def __init__(self):
        self.states = {}
        self.transitions = {}
        self.cur_state = None
        self.trans = None

    def set_state(self, state_name):
        self.cur_state = self.states[state_name]

    def transition(self, trans_name):
        self.trans = self.transitions[trans_name]

    def execute(self):
        if self.trans:
            self.trans.execute()
            self.set_state(self.trans.to_state)
            self.trans = None
        self.cur_state.execute()
