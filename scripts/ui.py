from scripts.downloader import Downloader
from modules import script_callbacks
import gradio as gr
from modules.paths_internal import models_path
from modules.sd_models import model_path
from modules.sd_vae import vae_path

options = ['Checkpoint', 'Lora', 'VAE']


def download(download_url, model_type, save_file_name):
    if download_url == '' or download_url is None:
        gr.Warning("请输入模型下载地址")
        return False
    if save_file_name == '' or save_file_name is None:
        gr.Warning("请输入保存的文件名")
        return False
    base_path = ''
    if model_type == 'Checkpoint':
        base_path = model_path
    elif model_type == 'VAE':
        base_path = vae_path
    elif model_type == 'Lora':
        base_path = f"{models_path}/Lora"
    path = f"{base_path}/{save_file_name}"
    downloader = Downloader(download_url, path)
    downloader.start()


def ui_tab():
    with gr.Blocks(analytics_enabled=False) as tab:
        with gr.Row():
            with gr.Column():
                download_url = gr.Textbox(label="模型下载地址", placeholder="输入模型下载地址")
        with gr.Row():
            with gr.Column():
                model_type = gr.Dropdown(label="模型类型", choices=options, value="Checkpoint")
            with gr.Column():
                save_file_name = gr.Textbox(label="保存的文件名", placeholder="输入保存的文件名")
        with gr.Row():
            with gr.Column():
                download_click = gr.Button(value="下载")
                download_click.click(download, inputs=[download_url, model_type, save_file_name])
        return [(tab, "模型下载助手", "model_help")]


script_callbacks.on_ui_tabs(ui_tab)
