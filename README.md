# Py9Gag
This script downloads a series of random images from [9Gag](http://9gag.com/)
and stores them in the given output directory. Files are ordered numerically
after the program was started. You need to be cautious because it will overwrite
images that were generated in a previous run.

## Running the script
```
git clone https://github.com/KonstantinRr/Py9Gag && cd Py9Gag
pip install requirements.txt
python main.py
```

## Requirements for this script
The project relies on a list of dependencies to download and render
the JavaScript content. It uses the Qt5 package to achieve this.

- PyQt5
- PyQt5WebKit (not necessary if you do not want to render the content)
- PyQtWebEngine
- lxml
- bs4
