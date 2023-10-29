import json
import os
import sys
from pathlib import Path
from functools import partial
import importlib
import gradio as gr
import traceback
from modules import shared
import webbrowser

model_name = 'None'
color_er = gr.themes.colors.blue

theme = gr.themes.Default(
    primary_hue=gr.themes.colors.orange,
    neutral_hue=gr.themes.colors.gray,
    secondary_hue=gr.themes.colors.pink,
    font=['Helvetica', 'ui-sans-serif', 'system-ui', 'sans-serif'],
    font_mono=['IBM Plex Mono', 'ui-monospace', 'Consolas', 'monospace'],
).set(

    # Colors
    input_background_fill_dark="*neutral_800",
    button_cancel_border_color=color_er.c200,
    button_cancel_border_color_dark=color_er.c600,
    button_cancel_text_color=color_er.c600,
    button_cancel_text_color_dark="white",
)

def download_model_wrapper(repo_id, specific_file, progress=gr.Progress(), return_links=False, check=False):
    try:
        downloader_module = importlib.import_module("download-model")
        downloader = downloader_module.ModelDownloader()

        progress(0.0)
        yield ("Cleaning up the model/branch names")
        model, branch = downloader.sanitize_model_and_branch_names(repo_id, None)

        yield ("Getting the download links from Hugging Face")
        links, sha256, is_lora, is_llamacpp = downloader.get_download_links_from_huggingface(model, branch, text_only=False, specific_file=specific_file)

        if return_links:
            yield '\n\n'.join([f"`{Path(link).name}`" for link in links])
            return

        yield ("Getting the output folder")
        base_folder = shared.args.lora_dir if is_lora else shared.args.model_dir
        output_folder = downloader.get_output_folder(model, branch, is_lora, is_llamacpp=is_llamacpp, base_folder=base_folder)

        if check:
            progress(0.5)
            yield ("Checking previously downloaded files")
            downloader.check_model_files(model, branch, links, sha256, output_folder)
            progress(1.0)
        else:
            yield (f"Downloading file{'s' if len(links) > 1 else ''} to `{output_folder}/`")
            downloader.download_model_files(model, branch, links, sha256, output_folder, progress_bar=progress, threads=1, is_llamacpp=is_llamacpp)
            yield ("Done!")
    except:
        progress(1.0)
        yield traceback.format_exc().replace('\n', '\n\n')




with gr.Blocks(title="Downloader", theme=theme) as demo:
    gr.HTML("<h1>Download Model</h1>")
    with gr.Column():
        custom_model_menu = gr.Textbox(label="Download model or LoRA", info="Enter the Hugging Face username/model path, for instance: facebook/galactica-125m. To specify a branch, add it at the end after a \":\" character like this: facebook/galactica-125m:main. To download a single file, enter its name in the second box.", interactive=True)
        download_specific_file = gr.Textbox(placeholder="File name (for GGUF models)", show_label=False, max_lines=1, interactive=True)

    with gr.Row():
        download_model_button = gr.Button("Download", variant='primary', interactive=True)
        get_file_list = gr.Button("Get file list", interactive=True)
    with gr.Row():
        model_status = gr.Markdown('Ready')


    download_model_button.click(download_model_wrapper, [custom_model_menu, download_specific_file], model_status, show_progress=True)
    get_file_list.click(partial(download_model_wrapper, return_links=True), [custom_model_menu, download_specific_file], [model_status], show_progress=True)
 
demo.queue(concurrency_count=1)
demo.launch(server_port=7861,inbrowser=True)