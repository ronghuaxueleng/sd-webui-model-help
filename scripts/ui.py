from scripts.downloader import Downloader

import shutil
from modules import script_callbacks
import gradio as gr
from modules.paths_internal import models_path
from modules.sd_models import model_path
from modules.sd_vae import vae_path

options = ['Checkpoint', 'Lora', 'VAE']


def download(download_url, model_type, save_file_name, progress=gr.Progress(track_tqdm=True)):
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


def generate_file(file_obj, model_type):
    base_path = ''
    if model_type == 'Checkpoint':
        base_path = model_path
    elif model_type == 'VAE':
        base_path = vae_path
    elif model_type == 'Lora':
        base_path = f"{models_path}/Lora"
    print('上传文件的地址：{}'.format(file_obj.name))  # 输出上传后的文件在gradio中保存的绝对地址
    shutil.move(file_obj.name, base_path)


def ui_tab():
    with gr.Blocks(analytics_enabled=False) as tab:
        with gr.Tabs():
            with gr.Tab(label='模型下载', elem_id="model_download_tab"):
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
                with gr.Row():
                    result = gr.Label(label="下载结果")
                download_click.click(download, inputs=[download_url, model_type, save_file_name], outputs=[result])
            with gr.Tab(label='模型上传', elem_id="model_upload_tab"):
                with gr.Row():
                    inputs = gr.File(label="上传文件")
                with gr.Row():
                    with gr.Column():
                        model_type = gr.Dropdown(label="模型类型", choices=options, value="Checkpoint")
                with gr.Row():
                    with gr.Column():
                        upload_click = gr.Button(value="上传")
                        upload_click.click(generate_file, inputs=[inputs, model_type])

        return [(tab, "模型下载助手", "model_help")]


script_callbacks.on_ui_tabs(ui_tab)
