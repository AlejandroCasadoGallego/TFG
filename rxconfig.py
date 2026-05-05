import os
import reflex as rx

database_url = os.environ.get("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/sistema_tareas")

config = rx.Config(
    app_name="TFG_Reflex",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url=database_url
)