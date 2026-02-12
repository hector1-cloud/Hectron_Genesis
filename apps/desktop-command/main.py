import flet as ft

def main(page: ft.Page):
    page.title = "HECTRON COMMAND"; page.theme_mode = ft.ThemeMode.DARK
    page.add(ft.Text("SYSTEM ONLINE", color="green"))

if __name__ == "__main__": ft.app(target=main)
