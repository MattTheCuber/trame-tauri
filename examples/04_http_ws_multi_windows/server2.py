from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html, tauri
from trame.widgets import vuetify3 as v3


@TrameApp()
class TestApp:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.state.update(
            {
                "position": None,
                "size": None,
                "scale": 0,
            }
        )
        tauri.initialize(self.server)
        self.build_ui_main()
        self.build_ui_hello_world()

    def build_ui_main(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            with layout.toolbar.clear():
                v3.VToolbarTitle("Multi Window example")
                v3.VSpacer()

                v3.VSpacer()
                v3.VBtn(
                    "Open Hello World",
                    disabled=("window_hello_world", False),
                    click="window_hello_world = true",
                )
                v3.VBtn(
                    "Close Hello World",
                    disabled=("!window_hello_world",),
                    click="window_hello_world = false",
                )
            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        v3.VCardTitle("Main Page")
                        with tauri.Window(main=True) as w:
                            with v3.Template(
                                raw_attrs=['v-slot="{ position, size, scaleFactor }"']
                            ):
                                html.Div(
                                    "{{ position }} | {{ size }} | {{ scaleFactor }}"
                                )

                html.Div("URL: {{ window.location }}")
                html.Div("p({{ position }}) - s({{ size }}) - d({{ scale }})")
                with tauri.Window(
                    url="http://localhost:4444/index.html?ui=hello_world",
                    visible=("window_hello_world", False),
                    title="Hello",
                    width=300,
                    height=300,
                    X=100,
                    y=100,
                    options=(
                        {
                            "alwaysOnTop": True,  # Does not work
                            "center": True,  # Does not work
                            "closable": False,  # Does not work
                            "decorations": False,  # Does not work
                            "focus": False,  # Does not work
                            "minHeight": 200,
                            "minWidth": 200,
                            "maxHeight": 800,
                            "maxWidth": 800,
                            "maximizable": False,  # Does not work
                            "minimizable": False,  # Does not work
                            "skipTaskbar": True,  # Does not work
                            "theme": "light",
                            "fileDropEnabled": False,  # Does not work
                        },
                    ),
                    prevent_close=True,  # Does not work
                    moved="position = $event",
                    resized="size = $event",
                    scale_changed="scale = $event",
                    created="{ position, size, scaleFactor: scale } = $event",
                    closed="window_hello_world = false",
                    file_drop="console.log('file:', $event)",
                    focus_changed="console.log('focus:', $event)",
                    theme_changed="console.log('theme:', $event)",
                ) as w:
                    with v3.Template(raw_attrs=['v-slot="data"']):
                        v3.VBtn("Center", click=w.center)
                        v3.VBtn("Show", click=w.show)
                        v3.VBtn("Hide", click=w.hide)
                        v3.VBtn("Maximize", click=w.maximize)
                        v3.VBtn("Un-Maximize", click=w.unmaximize)
                        v3.VBtn("Minimize", click=w.minimize)
                        v3.VBtn("Un-Minimize", click=w.unminimize)
                        v3.VBtn("Focus", click=w.grab_focus)
                        v3.VBtn("Fullscreen On", click=lambda: w.set_fullscreen(True))
                        v3.VBtn("Fullscreen Off", click=lambda: w.set_fullscreen(False))
                        v3.VBtn(
                            "Request User's Attention",
                            click=lambda: w.request_user_attention(2),
                        )
                        v3.VBtn("Set Position", click=lambda: w.set_position(0, 0))
                        v3.VBtn("Set Size", click=lambda: w.set_size(400, 400))
                        v3.VBtn("Set Title", click=lambda: w.set_title("World"))
                        html.Div("{{ data }}")

    def build_ui_hello_world(self):
        with SinglePageLayout(
            self.server, template_name="hello_world", full_height=True
        ) as layout:
            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        v3.VCardTitle("Hello World!")


if __name__ == "__main__":
    app = TestApp()
    app.server.start(port=4444, open_browser=False)
