class Testing:
    def __init__(self, persoon):
        self.state = persoon

    @classmethod
    def from_weerwolf(cls, state_given):
        cls.state = state_given


class Player:
    def __init__(self, name, id, role, permissions):
        self.name = name
        self.id = id
        self.role = role
        self.permissions = permissions
