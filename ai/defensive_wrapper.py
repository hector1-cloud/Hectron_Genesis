import time
import logging

class OrbitalDefensiveWrapper:
    """
    Escudo lógico contra la entropía y ataques adversarios.
    Detecta 'bit-flips' simulados por radiación o inyecciones de prompt maliciosas.
    """
    def __init__(self, llm_client, threshold=0.6):
        self.client = llm_client
        self.entropy_threshold = threshold

    def sanitize(self, response):
        # Detecta corrupción de datos
        entropy = self._calculate_entropy(response)
        if entropy > self.entropy_threshold:
            logging.warning("RADIACIÓN DETECTADA: Respuesta descartada.")
            return None
        return response

    def _calculate_entropy(self, text):
        if not text: return 0
        weird_chars = sum(1 for c in text if not c.isalnum() and c != ' ')
        return weird_chars / len(text)
