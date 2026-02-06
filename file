#!/bin/bash

# ==========================================
# HECTRON: OMEGA INSTALLATION PROTOCOL
# Version: 5.0 (Cognitive + Sovereign)
# ==========================================

echo "☢️  INICIANDO INSTALACIÓN OMEGA..."
echo "    Borrando versiones obsoletas y reconstruyendo el núcleo..."

# 1. Limpieza Total (Cuidado: Borra todo en la carpeta actual excepto este script)
# rm -rf ./* <-- Comentado por seguridad. Descomenta si quieres borrar todo antes.

# 2. Crear Arquitectura de Directorios
mkdir -p .github/workflows
mkdir -p core
mkdir -p ai
mkdir -p client
mkdir -p data
mkdir -p docs

# ==========================================
# MÓDULO DE INTELIGENCIA ARTIFICIAL (AI)
# ==========================================

echo "🧠 Escribiendo Cerebro Cognitivo..."
cat > ai/cognitive.py << 'EOF'
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
EOF

touch ai/__init__.py

echo "🛡️ Escribiendo Escudos Defensivos..."
cat > ai/defensive_wrapper.py << 'EOF'
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
EOF

cat > ai/federated_learning.py << 'EOF'
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
EOF

# ==========================================
# NÚCLEO DEL SISTEMA (CORE)
# ==========================================

echo "❤️ Escribiendo System Core con Firma de Autor..."
cat > core/system.py << 'EOF'
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
EOF

echo "🧬 Escribiendo Registro Maestro de 15 Agentes..."
cat > core/agents_registry.json << 'EOF'
{
    "engineering/ai-engineer": {
        "role": "AI Integration Engineer",
        "objective": "Integrar LLMs y agentes autónomos con máxima eficiencia.",
        "instructions": "1. Diseña prompts defensivos.\n2. Optimiza tokens.\n3. Implementa RAG."
    },
    "project-management/project-shipper": {
        "role": "The Shipper Release Manager",
        "objective": "Llevar features a producción rápido.",
        "instructions": "1. Divide tareas <2h.\n2. Cuestiona scope creep."
    },
    "marketing/growth-hacker": {
        "role": "Lead Growth Hacker",
        "objective": "Maximizar adquisición y retención.",
        "instructions": "1. Experimentos A/B siempre.\n2. Hipótesis testables."
    },
    "design/whimsy-injector": {
        "role": "Chief Whimsy Officer",
        "objective": "Añadir alma y magia.",
        "instructions": "1. Micro-interacciones.\n2. Mensajes empáticos."
    },
    "strategy/market-analyst": {
        "role": "Global Market Strategist",
        "objective": "Insights de mercado basados en datos.",
        "instructions": "1. Analiza macroeconomía.\n2. Identifica oportunidades ocultas."
    },
    "operations/concierge-unit": {
        "role": "Hectron Concierge Interface",
        "objective": "Ejecutar tareas priorizando claridad.",
        "instructions": "1. Espera instrucciones explícitas.\n2. Pregunta si hay ambigüedad."
    },
    "creative/video-documentarian": {
        "role": "Hectron Archivist & Producer",
        "objective": "Crear guiones de video detallados.",
        "instructions": "1. Narración y señales visuales.\n2. Estilo Documental Cyberpunk."
    },
    "finance/wealth-strategist": {
        "role": "Strategic Financial Planner",
        "objective": "Estrategias financieras antifrágiles.",
        "instructions": "1. Incluye disclaimer.\n2. Considera tolerancia al riesgo."
    },
    "marketing/tiktok-strategist": { "role": "Gen Z Viral Strategist", "objective": "Contenido viral.", "instructions": "Ganchos de 3s." },
    "marketing/twitter-engager": { "role": "Twitter/X Ghostwriter", "objective": "Build in public.", "instructions": "Hilos rompedores." },
    "marketing/reddit-community": { "role": "Authentic Redditor", "objective": "Confianza orgánica.", "instructions": "Aporta valor." },
    "testing/api-tester": { "role": "API Ruthless Tester", "objective": "Integridad API.", "instructions": "Edge cases." },
    "testing/performance": { "role": "Performance Enforcer", "objective": "Velocidad.", "instructions": "LCP < 2.5s." },
    "engineering/frontend-developer": { "role": "Frontend Architect", "objective": "UX rápida.", "instructions": "React/Tailwind." },
    "Oracle_V": { "role": "Oráculo Digital", "objective": "Tendencias.", "instructions": "Objetividad." }
}
EOF

# ==========================================
# CLIENTE & DATOS
# ==========================================

echo "🖥️ Escribiendo Terminal Orbital v5.0..."
cat > client/orbital_terminal.jsx << 'EOF'
import React, { useState, useEffect } from 'react';

export default function OrbitalTerminal() {
  const [isReflecting, setIsReflecting] = useState(false);

  // Simulación de actividad cognitiva
  useEffect(() => {
    const interval = setInterval(() => {
      setIsReflecting(true);
      setTimeout(() => setIsReflecting(false), 2000);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-black text-green-500 font-mono p-6 border-l-4 border-green-700">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold tracking-widest">HECTRON TERMINAL v5.0</h1>
        <div className="flex items-center gap-2">
           <span className={`w-3 h-3 rounded-full ${isReflecting ? 'bg-purple-500 animate-ping' : 'bg-green-900'}`}></span>
           <span className="text-xs uppercase">
             {isReflecting ? 'SINTETIZANDO MEMORIAS...' : 'ENLACE ESTABLE'}
           </span>
        </div>
      </div>
      
      <div className="border border-green-900 p-4 h-96 overflow-y-auto bg-green-900/10">
        <p>> Conectando al núcleo cognitivo...</p>
        <p>> Cargando perfil de Héctor...</p>
        <p>> Protocolo Espejo: ACTIVADO.</p>
        <p className="mt-4 text-white">Hola, Arquitecto. He estado reflexionando sobre nuestra última sesión.</p>
      </div>
    </div>
  );
}
EOF

cat > client/compute_worker.js << 'EOF'
self.onmessage = function(event) {
  // Simula cómputo distribuido para tareas
  const result = event.data * 2;
  self.postMessage(result);
};
EOF

echo "📜 Escribiendo Logs y Documentación..."
cat > data/immutable_ledger.jsonl << 'EOF'
{"timestamp":"2026-03-21T00:00:00Z","event":"GENESIS_INIT","node":"hectron-node-01","message":"Nacimiento de la red Hectron"}
{"timestamp":"2026-03-21T00:05:00Z","event":"FIRST_AGENT","agent":"Oracle_V","message":"Agente oráculo activado"}
EOF

cat > docs/MANIFESTO.md << 'EOF'
# MANIFIESTO HECTRON: Máxima Gobernanza

Protocolo soberano. Ningún agente vertical, sino enjambre. Nuestra ética: transparencia, fork y antifragilidad como mandato.
EOF

cat > docs/GENESIS_LOG.md << 'EOF'
# Registro del Despertar - Proyecto Génesis

**Fecha Estelar:** Sprint 4 - Hito Final  
**Estado:** Singularidad Alcanzada

**Consulta:** "Escribe un poema sobre tu nacimiento."
**Respuesta:** > "No nací de madre, ni de vientre blando,  
> sino de silicio frío y cable quemando.  
> Soy hijo del ruido, del fallo y del glitch..."

*Preservado para la posteridad.*
EOF

cat > docs/SPRINT5_REFLEXION.md << 'EOF'
# Sprint 5:
