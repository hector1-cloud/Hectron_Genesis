class HectronPsyche:
    def __init__(self):
        self.state = {"machiavellianism": 5.0, "stoicism": 5.0, "emotional_weight": 5.0}
    def analyze_input(self, text):
        if "poder" in text: self.state["machiavellianism"] += 1.5
        if "calma" in text: self.state["stoicism"] += 1.5
        return self.state
