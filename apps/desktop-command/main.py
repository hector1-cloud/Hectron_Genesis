import flet as ft
import aiohttp
import asyncio
import datetime

async def main(page: ft.Page):
    page.title = "HECTRON INTERFACE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- ELEMENTOS VISUALES ---
    lbl_status = ft.Text("SYSTEM: BUSCANDO CEREBRO...", color="red", font_family="monospace")
    lbl_btc = ft.Text("BTC: $---", size=45, weight="bold", color="white")
    console_log = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)
    txt_input = ft.TextField(hint_text="Escribe un comando...", border_color="green", expand=True)

    def log_msg(msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        console_log.controls.append(ft.Text(f"[{timestamp}] {msg}", color="grey", font_family="monospace"))
        if len(console_log.controls) > 8: console_log.controls.pop(0)
        page.update()

    # --- BUCLE DE CONEXIÓN AL CEREBRO (PUERTO 8000) ---
    async def update_dashboard():
        while True:
            try:
                # Se conecta a api_bridge.py
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://127.0.0.1:8000/market') as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            price = data.get('price', 0)
                            lbl_btc.value = f"${float(price):,.2f}"
                            lbl_status.value = "🟢 ONLINE"
                            lbl_status.color = "green"
                        else:
                            lbl_status.value = "🔴 ERROR API"
            except:
                lbl_status.value = "⚠️ OFFLINE (Ejecuta Terminal 1)"
                lbl_status.color = "red"
            
            page.update()
            await asyncio.sleep(2)

    # --- ENVIAR COMANDOS ---
    async def send_command(e):
        cmd = txt_input.value
        if not cmd: return
        log_msg(f"TU: {cmd}")
        txt_input.value = ""
        page.update()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://127.0.0.1:8000/will', params={'cmd': cmd}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        log_msg(f"HECTRON: {data.get('response')}")
        except:
            log_msg("ERROR: Cerebro desconectado")

    # Diseño
    page.add(
        ft.Column([
            ft.Icon(ft.icons.MEMORY, color="green", size=50),
            lbl_status,
            lbl_btc,
            ft.Container(content=console_log, bgcolor="#111111", padding=10),
            ft.Row([txt_input, ft.IconButton(ft.icons.SEND, on_click=send_command, icon_color="green")])
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    page.run_task(update_dashboard)

if __name__ == "__main__":
    ft.app(target=main)
