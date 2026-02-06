class FederatedAggregator:
    """
    Agrega gradientes de entrenamiento desde múltiples nodos distribuidos.
    """
    def __init__(self):
        self.updates = []

    def submit_update(self, gradients):
        self.updates.append(gradients)

    def aggregate(self):
        # Lógica de agregación (por ejemplo, promedio simple)
        if not self.updates:
            return None
        return self.updates[0]
