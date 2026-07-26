import flet as ft
from core.abada_agent import HectronAgent, omega_matrix

agent = HectronAgent("Abada Node")

def main(page: ft.Page):
    page.title = "HECTRON-Ψ • Unicornio Negro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    log = ft.ListView(expand=True, spacing=12, auto_scroll=True)
    input_field = ft.TextField(hint_text="Escribe tu decreto de prosperidad soberana...", multiline=True, min_lines=3, border_radius=20, bgcolor="#1f1f1f")
    omega_display = ft.Text("1.618034", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)

    async def execute(e):
        if not input_field.value.strip(): return
        log.controls.append(ft.Text(f"🦏 Decreto: {input_field.value}", color=ft.Colors.AMBER_300))
        page.update()
        result = agent.decide(input_field.value)
        new_omega = omega_matrix()
        omega_display.value = f"{new_omega:.6f}"
        log.controls.append(ft.Text(f"✅ {result}", color=ft.Colors.WHITE))
        input_field.value = ""
        page.update()

    page.add(ft.Column([
        ft.Row([ft.Text("HECTRON-Ψ", size=40, weight=ft.FontWeight.BOLD), ft.Text("🦏", size=50)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Text("MATRIZ Ω CÓSMICA", size=18, color=ft.Colors.AMBER_400),
        omega_display,
        input_field,
        ft.ElevatedButton("ACTIVAR CUERNO NASAL • EJECUTAR VOLUNTAD", on_click=execute, expand=True, height=70, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700)),
        log
    ], spacing=20))

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
