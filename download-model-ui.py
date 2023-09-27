import json
import os
import re
import sys
from pathlib import Path
import importlib
import inquirer
from download-model import ModelDownloader
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


model_name = 'None'
progress_info = (0, 0)

refresh_ui = False
files_choices = []

def fetch_files_for_model(repo_id):
    print("Fetching files for model")
    try:
        downloader = ModelDownloader()
        repo_id_parts = repo_id.split(":")
        model = repo_id_parts[0] if len(repo_id_parts) > 0 else repo_id
        branch = repo_id_parts[1] if len(repo_id_parts) > 1 else "main"
        model, branch = downloader.sanitize_model_and_branch_names(model, branch)
        links, _, _, file_sizes = downloader.get_download_links_from_huggingface(model, branch)
        filenames = [link.rsplit('/', 1)[1] for link in links]
        print(f"Fetched {len(filenames)} files.")  # Debugging line
        return filenames, file_sizes
    except:
        return ["Error fetching files"]
    
def download_selected_files(repo_id, selected_files):
    global progress_info
    try:
        downloader = ModelDownloader()
        repo_id_parts = repo_id.split(":")
        model = repo_id_parts[0] if len(repo_id_parts) > 0 else repo_id
        branch = repo_id_parts[1] if len(repo_id_parts) > 1 else "main"
        links, sha256, is_lora, file_sizes = downloader.get_download_links_from_huggingface(model, branch)
        
        # Filtering links based on selected files
        selected_links = [link for link in links if link.rsplit('/', 1)[1] in selected_files]
        selected_sha256 = [s for s in sha256 if s[0] in selected_files]
        
        output_folder = downloader.get_output_folder(model, branch, is_lora)

        downloader.download_model_files(model, branch, selected_links, selected_sha256, output_folder, threads=1)
        return "Download completed!"
    except Exception as e:
        return f"Error: {str(e)}"
    
def convert_bytes_to_readable(size):
    # Converts bytes to a human readable string, like "2.5 MB" or "3.1 GB"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Hugging Face Model Downloader"), width={"size": 6, "offset": 3}),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.InputGroup([
            dbc.Input(id="model-name-input", placeholder="Enter the Hugging Face username/model path"),
            dbc.Button("Fetch Files", id="fetch-files-button", color="primary", n_clicks=0)
        ]), width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Checklist(id='files-checklist', options=[]), width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Button("Download Selected Files", id="download-button", color="success", n_clicks=0), width=4)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(html.Div(id='output-container'), width=6)
    ])
], fluid=True)

@app.callback(
    Output('files-checklist', 'options'),
    Input('fetch-files-button', 'n_clicks'),
    State('model-name-input', 'value')
)
def update_file_list(n_clicks, model_name):
    if n_clicks > 0 and model_name:
        files_choices, file_sizes = fetch_files_for_model(model_name)  # Update the function to return sizes too
        # Display file name and size in the checklist
        return [{"label": f"{f} ({convert_bytes_to_readable(file_sizes[f])})", "value": f} for f in files_choices]
    return []

@app.callback(
    Output('output-container', 'children'),
    Input('download-button', 'n_clicks'),
    State('model-name-input', 'value'),
    State('files-checklist', 'value')
)
def download_files(n_clicks, model_name, selected_files):
    if n_clicks > 0 and model_name and selected_files:
        try:
            response = download_selected_files(model_name, selected_files)
            return response
        except Exception as e:
            return f"Error downloading files: {e}"
    return "No files downloaded."

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

demo.queue(concurrency_count=1)
demo.launch(server_port=7861)
