# SimplifiedMD

### About
SimplifiedMD is a tool that performs extractive summarization on medical articles from WebMD as well as any user-provided medical text!

### Description
Extractive summarization is performed using the following features:
* Count of thematic words
* Position of sentence
* Length of sentence
* Position of sentence relative to its paragraph
* Count of proper nouns
* Count of numerals
* Term Frequency-Inverse Sentence Frequency (TF-ISF)
* Centroid sentence-sentence similarity

### How to run (using conda)
Set up a conda environment:
```bash
$ conda create --name YOUR_ENV_NAME python=2.7
```
Activate the environment:
```bash
$ source activate YOUR_ENV_NAME
```
Install all dependencies listed in requirements.txt:
```bash
$ pip install -r requirements.txt
```

To run locally:
```bash
$ python manage.py runserver
```
runserver will automatically default to the settings in `settings/development.py`. Different settings can be chosen as the target using the `--settings` flag.

**NOTE:** Application secrets are stored in an `.env` file in `simplifiedmd/`. In order to run the application, at minimum a `SECRET_KEY` and `DEVO_ALLOWED_HOSTS` must be provided to run locally:
```bash
SECRET_KEY=YOUR_DJANGO_SECRET_KEY
DEVO_ALLOWED_HOSTS=.localhost, 127.0.0.1
```

