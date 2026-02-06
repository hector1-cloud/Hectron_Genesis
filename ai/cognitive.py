import time
import random

class CognitiveReflector:
    """
    Implementación del 'Mirror Protocol'. 
    Permite al sistema recordar interacciones pasadas y sintetizar 'Insights' (Reflexiones)
    para ajustar su comportamiento futuro basándose en patrones de usuario.
    """
    def __init__(self):
        self.memory_stream = [] # Historial crudo de observaciones
        self.insights = []      # Verdades sintetizadas de alto nivel
        self.reflection_threshold = 15 # Puntos de importancia para detonar una reflexión

    def add_observation(self, content, importance_score=1):
        """
        Registra un evento en el flujo de memoria.
        importance_score (1-10): 1=Trivial, 10=Crítico/Emocional.
        """
        observation = {
            "id": len(self.memory_stream) + 1,
            "content": content,
            "created_at": time.time(),
            "importance": importance_score,
            "type": "observation"
        }
        self.memory_stream.append(observation)
        
        # Verificar si se debe detonar una reflexión
        self._check_reflection_trigger()

    def get_relevant_context(self):
        """
        Recupera los insights más recientes para inyectarlos en el prompt del agente.
        """
        if not self.insights:
            return "MEMORIA: [Sistema recién iniciado. Sin patrones detectados.]"
        
        recent_insights = self.insights[-3:]
        context_str = "\n".join([f"- {i['content']}" for i in recent_insights])
        return f"MEMORIA REFLEXIVA (LO QUE SABES DEL USUARIO):\n{context_str}"

    def _check_reflection_trigger(self):
        # Suma la importancia de las últimas 5 memorias
        recent_importance = sum(m['importance'] for m in self.memory_stream[-5:])
        
        if recent_importance > self.reflection_threshold:
            self._synthesize_insight()

    def _synthesize_insight(self):
        """
        Simulación: Toma observaciones recientes y genera una 'Verdad'.
        """
        # Lógica simulada de "Darse cuenta"
        observations = [m['content'] for m in self.memory_stream[-5:]]
        
        # Ejemplo de patrón detectado
        new_insight = {
            "content": f"INSIGHT: El usuario prefiere respuestas técnicas y directas. (Derivado de: {len(observations)} interacciones recientes).",
            "created_at": time.time(),
            "type": "reflection"
        }
        
        self.insights.append(new_insight)
        print(f"✨ [META-COGNICIÓN] Hectron ha reflexionado: {new_insight['content']}")
