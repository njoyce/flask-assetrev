Flask-AssetRev
===============

Flask-AssetRev is a ``Flask`` extension which adds support for mapping
pre-built, content hashed static assets from the source form to the hashed
version at runtime.

For example if your app served a simple script and css file on every page view,
such as:

```html
<html>
  <head>
    <script type="text/javascript" src="{{ url_for('static', filename='app.js') }}></script>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='app.css') }}</script>
  </head>
  <body></body>
</html>
```

Everything works perfectly in development and you deploy your app to
production. Users start complaining about errors and you realise that their
version of ``app.js`` is being cached somehow out of your control. You decide
that content hashing is the way to solve it. You use something like
``gulp-rev`` to produce the revved assets and move them in to the static
sub-folder at build time.

But now the template above doesn't work. Flask-AssetRev solves this problem.

Rewriting your template to:

```html
<html>
  <head>
    <script type="text/javascript" src="{{ asset_url('app.js') }}></script>
    <link rel="stylesheet" type="text/css" href="{{ asset_url('app.css') }}</script>
  </head>
  <body></body>
</html>
```

Using the code:

```python
# app.py

from flask import Flask, render_template
from flask.ext import assetrev

app = flask.Flask(__name__)

assetrev.AssetRev(app)

@app.route('/')
def index():
    return render_template('index.html')
```

Will work for every version of the assets that you deploy.

Configuration Options
---------------------

| Name | Description |
|------|-------------|
| ``ASSETREV_MANIFEST_FILE`` | The mapping of source to revved asset json file as generated by `gulp-rev` (or similar). It must be within the same directory tree as the main flask app. |
| ``ASSETREV_BASE_URL`` | The url to find the compiled assets. By default the same host will be used. This allows the assets to be in a completely different domain. |
| ``ASSETREV_BASE_PATH`` | The directory within which to find the compiled assets in the app's static_folder. |
| ``ASSETREV_RELOAD`` | Whether to reload the asset manifest per request. By default, this is the same as ``app.config['DEBUG']``. |

Developer Guide
===============

Setting up:

```bash
# assumes that virtualenvwrapper is installed
$ mkvirtualenv assetrev
(assetrev) $ pip install -r requirements_dev.txt
(assetrev) $ pip install -e .
```

Running the tests:

```bash
(assetrev) $ nosetests