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
