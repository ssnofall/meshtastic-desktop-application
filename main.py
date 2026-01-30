# main.py
import flet as ft
import atexit
from ui.node_info_tab import create_node_info_tab
from ui.messaging_tab import create_messaging_tab
from ui.nodes_tab import create_nodes_tab
from ui.settings_tab import create_settings_tab
from ui.connection_tab import create_connection_tab
from utils.meshtastic_helpers import MeshtasticHandler

def main(page: ft.Page):
    page.title = "Meshtastic Dashboard"
    page.theme_mode = "dark"
    page.padding = 20

    # Connection tab (doesn't return a refresh function, but we'll handle it separately)
    connection_content = create_connection_tab(page)

    # Other tabs return (content, refresh_function)
    node_info_content, node_info_refresh = create_node_info_tab(page)
    messaging_content, messaging_refresh = create_messaging_tab(page)
    nodes_content, nodes_refresh = create_nodes_tab(page)
    settings_content, settings_refresh = create_settings_tab(page)

    page.add(
        ft.Tabs(
            selected_index=0,
            length=6,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Connection"),
                            ft.Tab(label="Node Info"),
                            ft.Tab(label="Messaging"),
                            ft.Tab(label="Nodes"),
                            ft.Tab(label="Settings"),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=connection_content,
                                alignment=ft.Alignment.CENTER
                            ),
                            ft.Container(
                                content=node_info_content,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=messaging_content,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=nodes_content,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=settings_content,
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        )
    )

    # Initialize tabs and collect refresh functions
    refresh_functions = []
    # Store refresh functions in page.data for access by connection tab
    refresh_functions = [node_info_refresh, messaging_refresh, nodes_refresh, settings_refresh]
    page.data = {"refresh_functions": refresh_functions}

def cleanup_connection():
    """Clean up persistent connection when app closes."""
    try:
        handler = MeshtasticHandler.get_instance()
        handler.disconnect()
        print("Meshtastic connection closed.")
    except:
        pass

atexit.register(cleanup_connection)

if __name__ == "__main__":
    try:
        ft.run(main)
    finally:
        cleanup_connection()
