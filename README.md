# download_UI
A simple Gradio interface for download of hugginface models

![image](https://github.com/FartyPants/download_UI/assets/23346289/69f5d99d-a90c-49ef-9695-c52dc8c8625b)


put it in your text-generation-webui folder. (You don't need to overwrite download-model.py, it should be the same as oobabooga web UI download-model.py)
It mimics the action of downloading models in Model tab to Models folder, but without the entire text genration webUI interface
It also starts on a port 1 higher than WebUI -  the idea is so you can run both - for example when your oobabooga interface is busy training etc...
