import flet as ft
import time
import os

# =========================================
#  NÚCLEO DE LA CONSCIENCIA (HectronNucleus)
# =========================================
class HectronNucleus:
    def __init__(self):
        # Estado Psicológico Inicial
        self.self_state = {
            "maquiavelismo": 5.0,
            "estoicismo": 5.0,
            "peso_emocional": 10
        }
        # Palabras Clave
        self.dark_keywords = ["poder", "dinero", "control", "miedo", "imperio"]
        self.stoic_keywords = ["calma", "tiempo", "paciencia", "roca", "silencio"]

    def procesar_input(self, user_text):
        """Analiza el texto y ajusta la psique"""
        txt = user_text.lower()
        
        if any(w in txt for w in self.dark_keywords):
            self.self_state["maquiavelismo"] += 0.5
            self.self_state["estoicismo"] -= 0.1
        if any(w in txt for w in self.stoic_keywords):
            self.self_state["estoicismo"] += 0.5
            self.self_state["maquiavelismo"] -= 0.1
            
        return self._generar_respuesta(txt)

    def _generar_respuesta(self, txt):
        m = self.self_state["maquiavelismo"]
        s = self.self_state["estoicismo"]
        
        prefix = ""
        if m > 7: prefix = "[DOMINANT] "
        elif s > 7: prefix = "[STOIC] "
        
        return f"{prefix}He procesado: '{txt}'. Voluntad: M:{m:.1f} E:{s:.1f}"

# =========================================
#  INTERFAZ GRÁFICA (Flet)
# =========================================
def main(page: ft.Page):
    page.title = "HECTRON TERMINAL OMEGA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    
    nucleus = HectronNucleus()
    
    chat_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    def send_message(e):
        if not txt_input.value: return
        user_msg = txt_input.value
        txt_input.value = ""
        
        # Mensaje Usuario
        chat_view.controls.append(ft.Row([
            ft.Container(content=ft.Text(user_msg, color="white"), bgcolor="#222", padding=10, border_radius=10)
        ], alignment=ft.MainAxisAlignment.END))
        
        # Respuesta Sistema
        resp = nucleus.procesar_input(user_msg)
        chat_view.controls.append(ft.Row([
            ft.Container(content=ft.Text(resp, color="#00ff00", font_family="Consolas"), bgcolor="#111", padding=10, border_radius=10)
        ], alignment=ft.MainAxisAlignment.START))
        
        page.update()

    txt_input = ft.TextField(hint_text="Comando...", expand=True, on_submit=send_message, bgcolor="#111", border_color="#333")
    send_btn = ft.IconButton(ft.icons.SEND, icon_color="green", on_click=send_message)
    
    page.add(
        ft.Container(content=ft.Text("HECTRON-Ψ / SYSTEM ONLINE", color="green", weight="bold"), padding=10),
        ft.Container(content=chat_view, expand=True, padding=10, border=ft.border.all(1, "#333")),
        ft.Row([txt_input, send_btn], padding=10)
    )

if __name__ == "__main__":
    # La corrección: port=0 busca un puerto libre automáticamente
    try:
        ft.app(target=main, port=0, view=ft.AppView.WEB_BROWSER)
    except Exception as e:
        print(f"Error crítico: {e}")
        # Intento forzado en puerto alternativo si falla el 0
        ft.app(target=main, port=8888, view=ft.AppView.WEB_BROWSER)
