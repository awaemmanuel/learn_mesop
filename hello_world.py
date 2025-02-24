import mesop as me

@me.page(path="/hello_world")
def app():
    """Hello World app using Mesop."""
    me.text(
        "Hello World!",
        type="headline-3",
        style=me.Style(
            font_size=36,
            font_weight=700,
            color="#000",
        ),
    )
    