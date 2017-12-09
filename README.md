# SimplifiedMD

### About
SimplifiedMD is a tool that performs extractive summarization on medical articles from WebMD.

### How to run (using conda)
Set up a conda environment:
```bash
conda create --name YOUR_ENV_NAME python=2.7
```
Activate the environment:
```bash
source activate YOUR_ENV_NAME
```
Install all dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
```

To run locally:
```bash
python manage.py runserver
```
runserver will automatically default to the settings in `settings/development.py`. Different settings can be chosen as the target using the `--settings` flag.

The server will be running on `localhost:8000`.
