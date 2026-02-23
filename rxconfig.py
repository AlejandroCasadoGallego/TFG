import reflex as rx

config = rx.Config(
    app_name="TFG_Reflex",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url="mysql+pymysql://root:@localhost:3306/sistema_tareas"
)