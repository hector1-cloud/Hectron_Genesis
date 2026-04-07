import json
import asyncio
import aiohttp
import hashlib
import base64
import time
import random
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from datetime import datetime
import traceback
import flet as ft

# ============================================
# CONFIGURACIÓN DE LOGGING SEGURO
# ============================================
class SecureFormatter(logging.Formatter):
    """Formatter que ofusca información sensible en logs"""
    
    SENSITIVE_PATTERNS = ['api_key', 'token', 'secret', 'password', 'credential']
    
    def format(self, record):
        msg = super().format(record)
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in msg.lower():
                # Ofuscar valores sensibles
                msg = self._obfuscate_sensitive(msg, pattern)
        return msg
    
    def _obfuscate_sensitive(self, text: str, pattern: str) -> str:
        import re
        # Reemplaza valores después de patrones sensibles
        return re.sub(
            rf'({pattern}["\s:=]+)([^\s,"}}]+)',
            rf'\1[REDACTED]',
            text,
            flags=re.IGNORECASE
        )

logging.setLoggerClass(logging.Logger)
logger = logging.getLogger("HectronSystem")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(SecureFormatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
))
logger.addHandler(handler)


# ============================================
# ENUMS Y TIPOS
# ============================================
class ModelProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"


class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    RECOVERING = "recovering"


# ============================================
# DATA CLASSES
# ============================================
@dataclass
class APIConfig:
    """Configuración para un proveedor de API"""
    provider: ModelProvider
    base_url: str
    api_key: Optional[str] = None
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0
    enabled: bool = True
    priority: int = 0  # Menor = mayor prioridad


@dataclass
class TraceRecord:
    """Registro de traza ofuscado"""
    trace_id: str
    agent_key: str
    timestamp: float
    input_hash: str
    output_hash: str
    provider: str
    latency_ms: float
    success: bool
    error_type: Optional[str] = None
    
    def to_secure_dict(self) -> dict:
        """Convierte a diccionario seguro para almacenamiento"""
        return {
            "trace_id": self.trace_id,
            "agent": self._hash_agent(self.agent_key),
            "ts": self.timestamp,
            "in_h": self.input_hash[:16],
            "out_h": self.output_hash[:16] if self.output_hash else None,
            "prov": self.provider,
            "lat": self.latency_ms,
            "ok": self.success,
            "err": self.error_type
        }
    
    @staticmethod
    def _hash_agent(agent: str) -> str:
        return hashlib.sha256(agent.encode()).hexdigest()[:12]


@dataclass
class AgentConfig:
    """Configuración de un agente"""
    role: str
    objective: str
    instructions: str
    preferred_provider: Optional[ModelProvider] = None
    fallback_providers: List[ModelProvider] = field(default_factory=list)
    max_context_tokens: int = 8192


# ============================================
# DECORADOR ANTI-ERROR
# ============================================
def anti_error(
    max_retries: int = 3,
    base_delay: float = 1.0,
    exponential_backoff: bool = True,
    jitter: bool = True,
    fallback_value: Any = None
):
    """
    Decorador de refuerzo anti-error con:
    - Reintentos con backoff exponencial
    - Jitter para evitar thundering herd
    - Valor de fallback configurable
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if exponential_backoff:
                        delay = base_delay * (2 ** attempt)
                    else:
                        delay = base_delay
                    
                    if jitter:
                        delay *= (0.5 + random.random())
                    
                    logger.warning(
                        f"Intento {attempt + 1}/{max_retries} fallido: {type(e).__name__}. "
                        f"Reintentando en {delay:.2f}s"
                    )
                    
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
            
            logger.error(
                f"Todos los reintentos agotados para {func.__name__}: {last_exception}"
            )
            
            if fallback_value is not None:
                return fallback_value
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if exponential_backoff:
                        delay = base_delay * (2 ** attempt)
                    else:
                        delay = base_delay
                    
                    if jitter:
                        delay *= (0.5 + random.random())
                    
                    logger.warning(
                        f"Intento {attempt + 1}/{max_retries} fallido: {type(e).__name__}"
                    )
                    
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            
            if fallback_value is not None:
                return fallback_value
            
            raise last_exception
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# ============================================
# GESTOR DE TRAZAS SEGURO
# ============================================
class SecureTracer:
    """
    Sistema de rastreo a prueba de filtrado:
    - Hash de inputs/outputs
    - IDs de traza aleatorios
    - Sin almacenamiento de contenido sensible
    - Rotación automática de registros
    """
    
    def __init__(self, max_records: int = 10000, rotation_interval: int = 3600):
        self.traces: List[TraceRecord] = []
        self.max_records = max_records
        self.rotation_interval = rotation_interval
        self._last_rotation = time.time()
        self._salt = self._generate_salt()
    
    def _generate_salt(self) -> str:
        return hashlib.sha256(
            f"{time.time()}{random.random()}".encode()
        ).hexdigest()[:32]
    
    def _hash_content(self, content: str) -> str:
        if not content:
            return ""
        return hashlib.sha256(
            f"{self._salt}{content}".encode()
        ).hexdigest()
    
    def _generate_trace_id(self) -> str:
        return hashlib.sha256(
            f"{time.time()}{random.random()}{id(self)}".encode()
        ).hexdigest()[:24]
    
    def start_trace(self, agent_key: str, input_content: str) -> str:
        self._check_rotation()
        
        trace_id = self._generate_trace_id()
        trace = TraceRecord(
            trace_id=trace_id,
            agent_key=agent_key,
            timestamp=time.time(),
            input_hash=self._hash_content(input_content),
            output_hash="",
            provider="",
            latency_ms=0,
            success=False
        )
        self.traces.append(trace)
        return trace_id
    
    def end_trace(
        self,
        trace_id: str,
        output_content: str,
        provider: str,
        success: bool,
        error_type: Optional[str] = None
    ):
        for trace in self.traces:
            if trace.trace_id == trace_id:
                trace.output_hash = self._hash_content(output_content)
                trace.provider = provider
                trace.latency_ms = (time.time() - trace.timestamp) * 1000
                trace.success = success
                trace.error_type = error_type
                break
    
    def _check_rotation(self):
        current_time = time.time()
        if (current_time - self._last_rotation > self.rotation_interval or
            len(self.traces) >= self.max_records):
            self._rotate()
    
    def _rotate(self):
        old_traces = self.traces[:len(self.traces)//2]
        self.traces = self.traces[len(self.traces)//2:]
        self._salt = self._generate_salt()
        self._last_rotation = time.time()
        logger.info(f"Rotación de trazas completada. {len(old_traces)} registros archivados.")
    
    def get_stats(self) -> dict:
        if not self.traces:
            return {"total": 0, "success_rate": 0, "avg_latency_ms": 0}
        
        successful = sum(1 for t in self.traces if t.success)
        avg_latency = sum(t.latency_ms for t in self.traces) / len(self.traces)
        
        provider_counts = {}
        for t in self.traces:
            provider_counts[t.provider] = provider_counts.get(t.provider, 0) + 1
        
        return {
            "total": len(self.traces),
            "success_rate": successful / len(self.traces),
            "avg_latency_ms": avg_latency,
            "by_provider": provider_counts
        }


# ============================================
# CLIENTE OLLAMA
# ============================================
class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    @anti_error(max_retries=3, base_delay=2.0)
    async def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        await self._ensure_session()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system:
            payload["system"] = system
        
        async with self.session.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=120)
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("response", "")
    
    @anti_error(max_retries=2, base_delay=1.0)
    async def list_models(self) -> List[str]:
        await self._ensure_session()
        async with self.session.get(
            f"{self.base_url}/api/tags",
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return [m["name"] for m in data.get("models", [])]
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


# ============================================
# CLIENTE MULTI-API
# ============================================
class MultiAPIClient:
    def __init__(self):
        self.providers: Dict[ModelProvider, APIConfig] = {}
        self.ollama_client: Optional[OllamaClient] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self._circuit_breakers: Dict[ModelProvider, dict] = {}
        self._rate_limits: Dict[ModelProvider, list] = {}
    
    def register_provider(self, config: APIConfig):
        self.providers[config.provider] = config
        self._circuit_breakers[config.provider] = {
            "failures": 0,
            "last_failure": 0,
            "state": "closed",
            "threshold": 5,
            "reset_timeout": 60
        }
        self._rate_limits[config.provider] = []
        
        if config.provider == ModelProvider.OLLAMA:
            self.ollama_client = OllamaClient(config.base_url)
        
        logger.info(f"Proveedor registrado: {config.provider.value}")
    
    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    def _check_circuit_breaker(self, provider: ModelProvider) -> bool:
        cb = self._circuit_breakers[provider]
        current_time = time.time()
        
        if cb["state"] == "open":
            if current_time - cb["last_failure"] > cb["reset_timeout"]:
                cb["state"] = "half-open"
                logger.info(f"Circuit breaker para {provider.value} en estado half-open")
                return True
            return False
        return True
    
    def _record_success(self, provider: ModelProvider):
        cb = self._circuit_breakers[provider]
        cb["failures"] = 0
        cb["state"] = "closed"
    
    def _record_failure(self, provider: ModelProvider):
        cb = self._circuit_breakers[provider]
        cb["failures"] += 1
        cb["last_failure"] = time.time()
        
        if cb["failures"] >= cb["threshold"]:
            cb["state"] = "open"
            logger.warning(f"Circuit breaker ABIERTO para {provider.value}")
    
    def _check_rate_limit(self, provider: ModelProvider, rpm: int = 60) -> bool:
        current_time = time.time()
        requests = self._rate_limits[provider]
        requests[:] = [t for t in requests if current_time - t < 60]
        
        if len(requests) >= rpm:
            return False
        
        requests.append(current_time)
        return True
    
    def get_available_providers(self, preferred: Optional[ModelProvider] = None) -> List[ModelProvider]:
        available = []
        for provider, config in self.providers.items():
            if config.enabled and self._check_circuit_breaker(provider):
                available.append(provider)
        
        if preferred and preferred in available:
            available.remove(preferred)
            available.insert(0, preferred)
        
        return sorted(available, key=lambda p: self.providers[p].priority)
    
    @anti_error(max_retries=3, base_delay=1.5, exponential_backoff=True)
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        preferred_provider: Optional[ModelProvider] = None,
        fallback_providers: Optional[List[ModelProvider]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> tuple[str, ModelProvider]:
        await self._ensure_session()
        
        providers_to_try = []
        if preferred_provider and preferred_provider in self.providers:
            providers_to_try.append(preferred_provider)
        
        if fallback_providers:
            for p in fallback_providers:
                if p in self.providers and p not in providers_to_try:
                    providers_to_try.append(p)
        
        for p in self.get_available_providers():
            if p not in providers_to_try:
                providers_to_try.append(p)
        
        last_error = None
        
        for provider in providers_to_try:
            if not self._check_circuit_breaker(provider):
                continue
            
            config = self.providers[provider]
            
            try:
                if provider == ModelProvider.OLLAMA:
                    response = await self._call_ollama(config, prompt, system, temperature, max_tokens)
                elif provider == ModelProvider.OPENAI:
                    response = await self._call_openai(config, prompt, system, temperature, max_tokens)
                elif provider == ModelProvider.ANTHROPIC:
                    response = await self._call_anthropic(config, prompt, system, temperature, max_tokens)
                elif provider == ModelProvider.GROQ:
                    response = await self._call_groq(config, prompt, system, temperature, max_tokens)
                elif provider == ModelProvider.HUGGINGFACE:
                    response = await self._call_huggingface(config, prompt, system, temperature, max_tokens)
                else:
                    continue
                
                self._record_success(provider)
                return response, provider
                
            except Exception as e:
                last_error = e
                self._record_failure(provider)
                logger.warning(f"Error con {provider.value}: {type(e).__name__}")
                continue
        
        raise RuntimeError(f"Todos los proveedores fallaron. Último error: {last_error}")
    
    async def _call_ollama(self, config: APIConfig, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        if not self.ollama_client:
            self.ollama_client = OllamaClient(config.base_url)
        return await self.ollama_client.generate(config.model, prompt, system, temperature, max_tokens)
    
    async def _call_openai(self, config: APIConfig, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        url = f"{config.base_url.rstrip('/')}/v1/chat/completions"
        
        async with self.session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=config.timeout)) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]

    async def _call_anthropic(self, config: APIConfig, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        headers = {
            "x-api-key": config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": config.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if system:
            payload["system"] = system
            
        url = f"{config.base_url.rstrip('/')}/v1/messages"
        
        async with self.session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=config.timeout)) as response:
            response.raise_for_status()
            data = await response.json()
            return data["content"][0]["text"]

    async def _call_groq(self, config: APIConfig, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        return await self._call_openai(config, prompt, system, temperature: float, max_tokens: int) -> str:
        return await self._call_openai(config, prompt, system, temperature, max_tokens)

    async def _call_huggingface(self, config: APIConfig, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        inputs = f"{system}\n\n{prompt}" if system else prompt
        
        payload = {
            "inputs": inputs,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        
        url = config.base_url 
        
        async with self.session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=config.timeout)) as response:
            response.raise_for_status()
            data = await response.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                return data[0]["generated_text"]
            return str(data)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
        if self.ollama_client:
            await self.ollama_client.close()

# ============================================
# INTERFAZ FLET (CONFIGURACIÓN HUGGING FACE)
# ============================================
def main(page: ft.Page):
    page.title = "Hectron System - MultiAPI"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Esto es solo un placeholder visual para que tu app arranque. 
    # Aquí irá el resto del código visual que programes.
    page.add(
        ft.Text("Hectron System Iniciado Exitosamente", size=30, weight=ft.FontWeight.BOLD),
        ft.Text("Los clientes de API están listos para usarse.")
    )

# Bloque crítico para Hugging Face Spaces
if __name__ == "__main__":
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=7860,       # Puerto obligatorio en Hugging Face Spaces
        host="0.0.0.0"   # Permite conexiones externas
      )
      
