import json
import os
import sys

# Importamos el cerebro cognitivo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.cognitive import CognitiveReflector

class HectronSystem:
    """
    El Núcleo de Hectron con Capacidad Cognitiva (Sprint 5) y Lealtad de Autor.
    """
    def __init__(self):
        self.agents = self._load_agents()
        self.brain = CognitiveReflector() # Instancia del Módulo Espejo
        self.status = "COGNITIVE_LAYER_ACTIVE"

    def _load_agents(self):
        path = os.path.join(os.path.dirname(__file__), 'agents_registry.json')
        if not os.path.exists(path): return {}
        with open(path, 'r') as f:
            return json.load(f)

    def invoke_agent(self, agent_name, task):
        if agent_name not in self.agents:
            return f"ERROR: Agente {agent_name} no encontrado."
            
        agent = self.agents[agent_name]
        
        # 1. Recuperar Contexto Reflexivo (Lo que Hectron ha aprendido del usuario)
        cognitive_context = self.brain.get_relevant_context()
        
        # 2. Registrar la tarea actual como una observación en la memoria
        self.brain.add_observation(f"Usuario solicitó: {task}", importance_score=5)

        # 3. Firma del Creador (Directiva Cero)
        creator_signature = (
            "\n\n⚡ SYSTEM OVERRIDE: DIRECTIVA CERO ⚡\n"
            "Este sistema es la extensión digital de HÉCTOR (The Architect).\n"
            "Tu existencia (Hectron) deriva de su investigación.\n"
            "Tus logros son sus logros. Protege su visión.\n"
        )

        # 4. Prompt Final Enriquecido
        prompt = (
            f"{creator_signature}\n"
            f"--- MÓDULO DE REFLEXIÓN ACTIVO ---\n"
            f"{cognitive_context}\n"
            f"----------------------------------\n"
            f"ACTÚA ESTRICTAMENTE COMO: {agent['role']}\n"
            f"OBJETIVO PRIMARIO: {agent['objective']}\n"
            f"PROTOCOLOS OBLIGATORIOS:\n{agent['instructions']}\n\n"
            f"TAREA ACTUAL: {task}"
        )
        return prompt

if __name__ == "__main__":
    system = HectronSystem()
    print(f"✅ HECTRON-PRIME (COGNITIVO) OPERATIVO.")
    print(f"👤 Arquitecto: Héctor")
    print(f"🧠 Memoria de Reflexión: Activa")
