import flet as ft
import google.generativeai as genai
import os

# --- CONFIGURACIÓN CENTRAL HECTRON ---
# Tu Credencial de Acceso (API Key)
API_KEY = "AIzaSyAJI3m1dXZuDqDasuLyHk5-xrLkoI8lCVw"

# Configuración del Modelo (Cerebro Moto AI)
try:
    genai.configure(api_key=API_KEY)
    # Usamos Gemini Flash: Rápido y ligero para el procesador del Edge 60
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_STATUS = True
except Exception as e:
    AI_STATUS = False
    print(f"Error de inicialización IA: {e}")

def main(page: ft.Page):
    # --- 1. Interfaz Visual (Estilo Cyberpunk/Hacker) ---
    page.title = "HECTRON-Ψ // TERMINAL"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"  # Negro absoluto
    page.padding = 20
    
    # Ajustes para pantalla móvil
    page.scroll = ft.ScrollMode.AUTO

    # Título del Sistema
    lbl_title = ft.Text("HECTRON-Ψ", size=24, weight="BOLD", color=ft.colors.CYAN_400, font_family="monospace")
    lbl_subtitle = ft.Text("MOTO AI // LINK ESTABLECIDO", size=12, color=ft.colors.GREEN_400)

    # Contenedor del Historial de Chat
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # --- 2. Lógica del Sistema ---
    
    def add_message(text, sender="SYSTEM"):
        # Colores según quién habla
        if sender == "TÚ":
            align = ft.MainAxisAlignment.END
            bg_color = ft.colors.BLUE_GREY_900
            txt_color = ft.colors.WHITE
        else: # HECTRON
            align = ft.MainAxisAlignment.START
            bg_color = ft.colors.GREY_900
            txt_color = ft.colors.CYAN_200

        # Burbuja de mensaje
        bubble = ft.Container(
            content=ft.Column([
                ft.Text(sender, size=10, weight="BOLD", color=ft.colors.GREY_500),
                ft.Markdown(text, selectable=True)
            ]),
            border_radius=10,
            padding=10,
            bgcolor=bg_color,
            border=ft.border.all(1, ft.colors.CYAN_900 if sender != "TÚ" else ft.colors.TRANSPARENT),
            width=300 # Ancho máximo para móvil
        )
        
        chat_list.controls.append(ft.Row([bubble], alignment=align))
        page.update()

    def send_prompt(e):
        user_text = txt_input.value
        if not user_text: return

        # 1. Mostrar mensaje del usuario
        txt_input.value = ""
        add_message(user_text, sender="TÚ")
        txt_input.focus()
        page.update()

        # 2. Procesar con IA
        if not AI_STATUS:
            add_message("⚠️ Error: La IA no pudo iniciarse. Verifica tu conexión.", sender="SISTEMA")
            return

        try:
            # Indicador de carga simple
            page.title = "HECTRON-Ψ (Procesando...)"
            page.update()

            response = model.generate_content(user_text)
            
            page.title = "HECTRON-Ψ // TERMINAL"
            add_message(response.text, sender="HECTRON")
            
        except Exception as err:
            add_message(f"Error en enlace neuronal: {err}", sender="ERROR")

    # --- 3. Componentes de Entrada ---
    txt_input = ft.TextField(
        hint_text="Ingresa comando...",
        hint_style=ft.TextStyle(color=ft.colors.GREY_700),
        bgcolor=ft.colors.GREY_900,
        color=ft.colors.CYAN_50,
        border_radius=15,
        border_color=ft.colors.CYAN_800,
        expand=True,
        on_submit=send_prompt
    )

    btn_send = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.CYAN_400,
        on_click=send_prompt
    )

    # Ensamblar la pantalla
    page.add(
        ft.Row([lbl_title], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([lbl_subtitle], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(color=ft.colors.CYAN_900),
        ft.Container(content=chat_list, expand=True), # El chat ocupa el espacio disponible
        ft.Divider(color=ft.colors.TRANSPARENT, height=5),
        ft.Row([txt_input, btn_send], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # Bienvenida
    add_message("Núcleo Hectron iniciado en Motorola Edge 60. Esperando instrucciones...", sender="SISTEMA")

# Ejecuta en modo navegador (ideal para Termux)
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
