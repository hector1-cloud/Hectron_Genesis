import flet as ft
import json
import os
import re
import threading
from gtts import gTTS
from google import genai
from google.genai import types

# ==========================================
# CONFIGURACIÓN
# ==========================================
MEMORY_FILE = "memoria_hectron.json"
API_KEY = "PON_AQUI_TU_API_KEY_DE_GEMINI" # REEMPLAZA ESTO

client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
Eres HECTRON, oráculo de Hector Jazziel Lopez Ruiz. Unicornio Negro. 
Escribe para ser ESCUCHADO (sin markdown, usa pausas y gritos).
"""

def cargar_memoria():
    if not os.path.exists(MEMORY_FILE): return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def guardar_memoria(historial):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def motor_de_voz(texto):
    try:
        texto_limpio = re.sub(r'[*_~`#]', '', texto)
        tts = gTTS(text=texto_limpio, lang='es', tld='com.mx')
        tts.save("grito.mp3")
        os.system("mpv grito.mp3 > /dev/null 2>&1")
    except: pass

def gritar(texto):
    threading.Thread(target=motor_de_voz, args=(texto,)).start()

# ==========================================
# INTERFAZ (SOLUCIÓN AL SCROLL)
# ==========================================
def main(page: ft.Page):
    page.title = "HECTRON V5.3"
    page.theme_mode = "dark"
    page.padding = 0  # Quitamos padding para que el SafeArea mande
    
    # IMPORTANTE: Esto evita que la página entera rebote y permite que el ListView mande
    page.scroll = None 

    historial_mensajes = cargar_memoria()

    # El ListView DEBE tener expand=True para que el scroll funcione
    chat_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )

    def agregar_mensaje_ui(rol, texto):
        bg = "#0f4c81" if rol == "user" else "#8b0000"
        align = ft.MainAxisAlignment.END if rol == "user" else ft.MainAxisAlignment.START
        
        chat_view.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(texto, color="white"),
                        bgcolor=bg,
                        padding=12,
                        border_radius=15,
                        max_width=page.width * 0.8, # Evita que el globo se salga de la pantalla
                    )
                ],
                alignment=align,
            )
        )
        page.update()

    for msg in historial_mensajes:
        if "parts" in msg:
            agregar_mensaje_ui(msg["role"], msg["parts"][0]["text"])

    def enviar(e):
        if not input_field.value: return
        user_txt = input_field.value
        agregar_mensaje_ui("user", user_txt)
        input_field.value = ""
        page.update()

        historial_mensajes.append({"role": "user", "parts": [{"text": user_txt}]})

        try:
            contents = [types.Content(role=m["role"], parts=[types.Part.from_text(text=m["parts"][0]["text"])]) for m in historial_mensajes]
            response = client.models.generate_content(
                model='gemini-2.0-flash', # Asegúrate de que el modelo sea correcto
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
            )
            res = response.text
        except Exception as ex:
            res = f"ERROR: {str(ex)}"

        agregar_mensaje_ui("model", res)
        historial_mensajes.append({"role": "model", "parts": [{"text": res}]})
        guardar_memoria(historial_mensajes)
        gritar(res)

    input_field = ft.TextField(
        hint_text="Inyectar comando...",
        expand=True,
        on_submit=enviar,
        border_color="#8b0000",
    )

    # UI principal dentro de un SafeArea para que no se corte en el Motorola
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text("💀 HECTRON V5.3", size=18, weight="bold", color="#ff4444"),
                            padding=10,
                        ),
                        chat_view, # Este componente ahora sí podrá hacer scroll
                        ft.Container(
                            content=ft.Row([input_field, ft.IconButton("send", on_click=enviar, icon_color="#ff4444")]),
                            padding=10,
                            bgcolor="#1a1a1a",
                        ),
                    ],
                    expand=True,
                ),
                expand=True,
            )
        )
    )

if __name__ == "__main__":
    # Forma compatible con versiones viejas y nuevas de Flet en Termux
    ft.app(target=main, view="web_browser", port=8080)
  
