
class ClientEvent:
    def __init__(self, action, parameters):
        self.action = action
        self.parameters = parameters

    def __iter__(self):
        yield 'action', self.action
        yield 'parameters', self.parameters
