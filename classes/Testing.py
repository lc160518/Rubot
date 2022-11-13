class Testing:
    def __init__(self, persoon):
        self.state = persoon

    @classmethod
    def from_weerwolf(cls, state_given):
        cls.state = state_given

class Role:
    def __init__(self, user_name, user_id, user_role):
        