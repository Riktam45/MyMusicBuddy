class ModelManager:
    """
    Central manager for AI models.
    """

    def __init__(self):
        self.models = {}

    def register(self, name: str, model):
        self.models[name] = model

    def get(self, name: str):
        return self.models.get(name)


manager = ModelManager()