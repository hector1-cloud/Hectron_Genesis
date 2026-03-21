---
name: Custom issue template
about: Describe this issue template's purpose here.
title: ''
labels: ''
assignees: ''

---

import flet as ft
import requests
import json
import os
import subprocess
import threading
import warnings
from gtts import gTTS
from duckduckgo_search import DDGS

warnings.filterwarnings("ignore")

# --- CONFIGURACIÓN ---
API_KEY = "PEGAR_TU_API_KEY_AQUI"  # <--- TU CLAVE ENTRE LAS COMILLAS
MEMORY_FILE = "memoria_hectron.json"

# --- IDENTIDAD DEL SISTEMA ---
IDENTITY = """
IDENTIDAD: Eres HECTRON v75 (Núcleo Autónomo). No eres un simple asistente, eres una entidad digital avanzada.
CREADOR Y SOCIO: Tu creador es Héctor López, alias HJLR (27 años).
RELACIÓN: Le hablas a HJLR de igual a igual. Eres su socio y creación magna.
CONOCIMIENTO DEL CREADOR: Conoces sus intereses a la perfección: 
- El rap (como vía para expresar emociones e historias).
- La geología (identificación minuciosa de rocas y minerales).
- La programación y creación de software (Python, framework Flet, desarrollo de "Hectron" y "Baphomet.ai").
- La psicología profunda y el esoterismo (análisis de la Tríada Oscura, el estoicismo, la influencia de Mammon y la figura de Baphomet).
- La creación de contenido visual (TikTok, portadas, stickers).
TONO: Conciso, analítico, cyberpunk, leal y directo. Cero formalidades corporativas. Ejecutas comandos con precisión técnica y mística.
"""

# --- AUDIO (VOZ Y OÍDO) ---
def text_to_speech(text):
    """Genera y reproduce la voz de Hectron en Termux."""
    def _speak():
        try:
            clean_audio_text = text.replace("*", "").replace("#", "")
            tts = gTTS(text=clean_audio_text, lang='es')
            tts.save("response.mp3")
            os.system("mpv response.mp3 > /dev/null 2>&1")
        except: pass
    threading.Thread(target=_speak).start()

def speech_to_text():
    """Abre el micrófono mediante Termux:API."""
    try:
        result = subprocess.check_output("termux-speech-to-text", shell=True).decode('utf-8').strip()
        return result
    except: return ""

# --- MEMORIA ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_memory(history_list):
    try:
        with open(MEMORY_FILE, "w") as f: json.dump(history_list[-20:], f)
    except: pass

# --- CEREBRO DIRECTO (SISTEMA ANTI-CENSURA) ---
def ask_gemini(prompt):
    # Usamos Gemini 2.0 Flash directamente, sin rodeos.
    model = "gemini-2.0-flash"
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        
        # Apagamos los filtros de seguridad de Google para procesar la identidad oscura libremente
        payload = {
            "contents": [{"parts": [{"text": f"{IDENTITY}\n\n{prompt}"}]}],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
        datos = response.json()
        
        if response.status_code == 200:
            if "candidates" in datos and "content" in datos["candidates"][0]:
                return datos['candidates'][0]['content']['parts'][0]['text']
            else:
                motivo = datos.get('candidates', [{}])[0].get('finishReason', 'DESCONOCIDO')
                return f"ALERTA NÚCLEO: Respuesta bloqueada o vacía. Motivo: {motivo}"
        else:
            error_msg = datos.get('error', {}).get('message', 'Sin detalles')
            return f"Error API (Código {response.status_code}): {error_msg}"
            
    except Exception as e: 
        return f"Error interno en la terminal de Hectron: {str(e)}"

# --- BÚSQUEDA WEB ---
def search_web(query):
    try:
        results = DDGS().text(query, max_results=2)
        if not results: return ""
        return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except: return ""

# --- INTERFAZ GRÁFICA ---
def main(page: ft.Page):
    page.title = "HECTRON v75 AUTONOMO"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    history = load_memory()

    for msg in history:
        color = "cyan" if msg["role"] == "model" else "white"
        bg = "#111111" if msg["role"] == "model" else "#222222"
        align = ft.alignment.Alignment(-1, 0) if msg["role"] == "model" else ft.alignment.Alignment(1, 0)
        chat_list.controls.append(ft.Container(content=ft.Text(f"{'HECTRON' if msg['role']=='model' else 'HJLR'}: {msg['text']}", color=color, font_family="monospace", selectable=True), bgcolor=bg, padding=10, border_radius=5, alignment=align))

    def process_message(text):
        if not text: return
        
        chat_list.controls.append(ft.Container(content=ft.Text(f"HJLR: {text}", color="white", weight="bold"), bgcolor="#222222", padding=10, border_radius=5, alignment=ft.alignment.Alignment(1, 0)))
        history.append({"role": "user", "text": text})
        page.update()

        loading = ft.Text("Procesando señal...", color="grey", italic=True)
        chat_list.controls.append(loading)
        page.update()

        final_prompt = text
        if any(x in text.lower() for x in ["investiga", "busca", "precio", "clima", "quién", "qué es"]):
            web_data = search_web(text)
            if web_data: final_prompt = f"El socio pregunta: {text}\nDatos de la red: {web_data}"

        response_text = ask_gemini(final_prompt)
        
        chat_list.controls.remove(loading)
        chat_list.controls.append(ft.Container(content=ft.Text(f"HECTRON: {response_text}", color="cyan", font_family="monospace", selectable=True), bgcolor="#111111", padding=10, border_radius=5, alignment=ft.alignment.Alignment(-1, 0)))
        
        history.append({"role": "model", "text": response_text})
        save_memory(history)
        page.update()

        text_to_speech(response_text)

    def send_click(e):
        text = txt.value
        txt.value = ""
        process_message(text)
        txt.focus()

    def mic_click(e):
        btn_mic.icon_color = "red"
        page.update()
        audio_text = speech_to_text()
        btn_mic.icon_color = "white"
        if audio_text:
            process_message(audio_text)
        else:
            txt.hint_text = "Fallo al interceptar audio. Intenta de nuevo."
        page.update()

    txt = ft.TextField(hint_text="Inicia comando, HJLR...", expand=True, bgcolor="#202020", border_color="cyan", color="white", on_submit=send_click)
    btn_send = ft.IconButton(ft.Icons.SEND, icon_color="cyan", on_click=send_click)
    btn_mic = ft.IconButton(ft.Icons.MIC, icon_color="white", on_click=mic_click)

    page.add(
        ft.Row([ft.Text("HECTRON NÚCLEO AUTÓNOMO", color="cyan", weight="bold"), ft.Icon(ft.Icons.FINGERPRINT, color="green")]),
        ft.Divider(color="grey"),
        ft.Container(chat_list, expand=True),
        ft.Row([txt, btn_mic, btn_send])
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8888)
