import reflex as rx
from .State import State
from .components.ui import login_page, index_page, landing_page, register_page
from .models import *

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="indigo")
)

app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(index_page, route="/dashboard", on_load=State.check_login)