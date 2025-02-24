""" Main DuoChat application. """

import mesop as me
from data_model import State, Models, ModelDialogState, Conversation, ChatMessage
from dialog import dialog, dialog_actions
import gemini
import claude

STYLE_SHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]

class DuoChatError(Exception):
    """Custom exception for DuoChat."""


def change_model_option(e: me.CheckboxChangeEvent):
    """Handle model option change."""
    state = me.state(ModelDialogState)
    if e.checked:
        state.selected_models.append(e.key)
    else:
        state.selected_models.remove(e.key)
    print(f"Selected models: {state.selected_models}")


def set_gemini_api_key(e: me.InputBlurEvent):
    """Set the Gemini API key."""
    state = me.state(State)
    state.gemini_api_key = e.value
    print(f"Gemini API Key: {state.gemini_api_key}")


def set_claude_api_key(e: me.InputBlurEvent):
    """Set the Claude API key."""
    state = me.state(State)
    state.claude_api_key = e.value
    print(f"Claude API Key: {state.claude_api_key}")


def model_picker_dialog():
    """Dialog for model picker."""
    state = me.state(State)
    with dialog(is_open=state.is_model_picker_dialog_open):
        with me.box(
            style=me.Style(
                display="flex",
                flex_direction="column",
                gap=12,
            )
        ):
            me.text("API Keys")
            me.input(
                label="Gemini API Key",
                value=state.gemini_api_key,
                on_blur=set_gemini_api_key,
                placeholder="Enter your Gemini API Key",
            )
            me.input(
                label="Claude API Key",
                value=state.claude_api_key,
                on_blur=set_claude_api_key,
                placeholder="Enter your Claude API Key",
            )
        me.text("Pick a model")
        for model in Models:
            if model.name.lower().startswith("gemini"):
                disabled = not state.gemini_api_key
            elif model.name.lower().startswith("claude"):
                disabled = not state.claude_api_key
            else:
                disabled = False
            me.checkbox(
                key=model.value,
                label=model.value,
                checked=model.value in state.models,
                disabled=disabled,
                on_change=change_model_option,
                style=me.Style(
                    display="flex",
                    flex_direction="column",
                    gap=4,
                    padding=me.Padding(top=12),
                ),
            )
        with dialog_actions():
            me.button("Cancel", on_click=close_model_picker_dialog)
            me.button("Confirm", on_click=confirm_model_picker_dialog)


def close_model_picker_dialog(event: me.ClickEvent):
    """Close the model picker dialog."""
    _ = event  # Unused event
    state = me.state(State)
    state.is_model_picker_dialog_open = False
    print("Model picker dialog closed.")


def confirm_model_picker_dialog(event: me.ClickEvent):
    """Confirm the model picker dialog."""
    _ = event  # Unused event
    dialog_state = me.state(ModelDialogState)
    state = me.state(State)
    state.is_model_picker_dialog_open = False
    state.models = dialog_state.selected_models
    print(f"Selected models: {state.models}")
    print("Model picker dialog confirmed.")


ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)


@me.page(
    path="/",
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
    ],
)
def page():
    """Main page of the app."""
    model_picker_dialog()
    with me.box(style=ROOT_BOX_STYLE):
        header()
        with me.box(
            style=me.Style(
                width="min(680px, 100%)",
                margin=me.Margin.symmetric(
                    horizontal="auto",
                    vertical=36,
                ),
            )
        ):
            me.text(
                "Chat with multiple models at once",
                style=me.Style(
                    font_size=20,
                    margin=me.Margin(bottom=24),
                ),
            )
            chat_input()
            display_conversations()


def display_conversations():
    """Display the conversations."""
    state = me.state(State)
    for conversation in state.conversations:
        with me.box(style=me.Style(margin=me.Margin(bottom=24))):
            me.text(f"Model: {conversation.model}", style=me.Style(font_weight=500))
            for message in conversation.messages:
                display_message(message)


def display_message(message):
    """Display a single message."""
    style = me.Style(
        padding=me.Padding.all(12),
        border_radius=8,
        margin=me.Margin(bottom=8),
    )
    if message.role == "user":
        style.background = "#e7f2ff"
    else:
        style.background = "#ffffff"
    with me.box(style=style):
        me.markdown(message.content)
        if message.in_progress:
            me.progress_spinner()


def header():
    """Header of the app."""
    with me.box(
        style=me.Style(
            padding=me.Padding.all(16),
        ),
    ):
        me.text(
            "DuoChat",
            style=me.Style(
                font_size=24,
                font_weight=500,
                background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
                color="#3D3929",
                letter_spacing="0.3px",
            ),
        )


def switch_model(e: me.ClickEvent):
    """Switch model event handler."""
    _ = e  # Unused event
    state = me.state(State)
    state.is_model_picker_dialog_open = True
    dialog_state = me.state(ModelDialogState)
    dialog_state.selected_models = state.models[:]
    print(f"Switching model: {state.models}")


def chat_input():
    """Chat input box for the application."""
    state = me.state(State)
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                value=state.input,
                on_blur=on_blur,
                placeholder="Type your message here...",
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
            with me.box(
                style=me.Style(
                    display="flex",
                    padding=me.Padding(left=12, bottom=12),
                    cursor="pointer",
                ),
                on_click=switch_model,
            ):
                me.text(
                    "Model:",
                    style=me.Style(font_weight=500, padding=me.Padding(right=6)),
                )
                if state.models:
                    me.text(", ".join(state.models))
                else:
                    me.text("(no model selected)")
        with me.content_button(
            type="icon", on_click=send_prompt, disabled=not state.models
        ):
            me.icon("send")


def on_blur(e: me.InputBlurEvent):
    """On blur event for the textarea."""
    state = me.state(State)
    state.input = e.value
    print(f"Input value: {state.input}")


def send_prompt(event: me.ClickEvent):
    """Send the prompt to the models."""
    _ = event  # Unused event
    state = me.state(State)
    if not state.conversations:
        for model in state.models:
            state.conversations.append(Conversation(model=model, messages=[]))
    prompt = state.input
    print(f"Sending prompt: {prompt}")
    state.input = ""

    for conversation in state.conversations:
        model = conversation.model
        messages = conversation.messages
        history = messages[:]
        messages.append(ChatMessage(role="user", content=prompt))
        messages.append(ChatMessage(role="model", in_progress=True))
        yield

        if model == Models.GEMINI_1_5_FLASH.value:
            llm_response = gemini.send_prompt(
                model="gemini-1.5-flash",
                prompt=prompt,
                history=history,
            )
        elif model == Models.GEMINI_2_0_FLASH.value:
            llm_response = gemini.send_prompt(
                model="gemini-2.0-flash",
                prompt=prompt,
                history=history,
            )
        elif model == Models.GEMINI_1_5_PRO.value:
            llm_response = gemini.send_prompt(
                model="gemini-1.5-pro",
                prompt=prompt,
                history=history,
            )
        elif model == Models.CLAUDE_3_5_SONNET.value:
            llm_response = claude.send_prompt(input, history)
        else:
            raise DuoChatError("Unhandled model", model)

        for chunk in llm_response:
            messages[-1].content += chunk
            yield
        messages[-1].in_progress = False
        yield
