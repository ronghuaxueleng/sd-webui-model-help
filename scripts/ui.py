from modules import script_callbacks
import gradio as gr


def ui_tab():
    with gr.Blocks(analytics_enabled=False) as tab:
        with gr.Row():
            with gr.Column():
                gr.HTML("", elem_id="iib_top")
        return [(tab, "模型下载助手", "model_help")]


script_callbacks.on_ui_tabs(ui_tab)
