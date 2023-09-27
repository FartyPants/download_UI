<h1>HuggingFace Model Downloader</h1>

<p>This project provides a simple GUI interface to download models from HuggingFace's Model Hub. It utilizes a <code>ModelDownloader</code> class for fetching and downloading the desired models and files, and a Dash-based GUI interface for smooth user interactions.</p>

![2023-09-23 08_50_27-Dash — Mozilla Firefox](https://github.com/magnumquest/download_UI2/assets/139659490/278f3ea7-ca0e-42e4-ab2d-9922e66ffda7)

<h2>Features</h2>

<ul>
    <li>Search for available files for a model. (GGUF and GGML Supported)</li>
    <li>Selectively download desired files.</li>
    <li>Streamlined user interface for better user experience.</li>
</ul>

<h2>Setup and Installation</h2>

<h3>Prerequisites</h3>

<ul>
    <li>Python 3.x</li>
    <li>Pip (Python package manager)</li>
</ul>

<h3>Instructions</h3>

<ol>
    <li><strong>Clone the Repository:</strong>
        <pre>
   git clone https://github.com/magnumquest/download_UI2.git
   cd download_UI2
        </pre>
    </li>
    <li><strong>Install Dependencies:</strong>
        <p>Ensure you have <code>pip</code> installed. Then, run:</p>
        <pre>
   pip install -r requirements.txt
        </pre>
        Then proceed with installing the dependencies as instructed above.
    </li>
    <li><strong>Run the GUI:</strong>
        <pre>
   python download-model-ui.py
        </pre>
        This will launch a web interface. Navigate to the provided URL (typically <code>http://127.0.0.1:8000/</code>), and you should see the Model Downloader GUI.
    </li>
</ol>

<h2>Usage</h2>

<ol>
    <li>Input the Hugging Face model name in the given text field.</li>
    <li>Click on 'Fetch Files' to retrieve the list of available files for the model.</li>
    <li>Select the files you wish to download from the checklist.</li>
    <li>Click on 'Download Selected Files' to start downloading the desired files.</li>
</ol>

<h2>Contributing</h2>

<p>Feel free to fork the project, make some updates, and submit pull requests. Any contributions are welcomed!</p>

