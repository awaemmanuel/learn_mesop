import mesop as me 


@me.stateclass
class CounterState:
    """State class to hold the counter value."""
    clicks: int = 0

def on_button_click(event: me.ClickEvent):
    """Handle button click event."""
    _ = event  # Unused event
    state = me.state(CounterState)
    state.clicks += 1
    
@me.page(path="/counter")
def main():
    """Counter app using Mesop."""
    state = me.state(CounterState)
    me.text(f"Button clicked {state.clicks} times")
    me.button(
        "Click Me",
        on_click=on_button_click,
    )
    