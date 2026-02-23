import reflex as rx
from .State import State
from .components.ui import login_page, index_page
from .models import *

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="indigo")
)

app.add_page(login_page, route="/", on_load=State.crear_usuario_prueba)
app.add_page(index_page, route="/dashboard", on_load=State.check_login)