import unittest

import flask
import flask_assetrev
from flask_assetrev import asset_url


def make_app(config=None, **kwargs):
    app = flask.Flask(__name__, **kwargs)

    config = config or {}

    app.config.update(config)

    app.config['TESTING'] = True
    app.config['ASSETREV_MANIFEST_FILE'] = 'my_assets.json'
    flask_assetrev.AssetRev(app)

    return app


class AssetRevTestCase(unittest.TestCase):
    def test_template(self):
        """
        Getting the asset_url from within a template should work.
        """
        app = make_app()

        with app.test_request_context():
            self.assertEqual(
                flask.render_template('index.html'),
                'http://localhost/static/app.deadb33f.js'
            )

    def test_programmatic(self):
        """
        Progmattically getting the asset_url should work.
        """
        app = make_app()

        with app.test_request_context():
            self.assertEqual(
                asset_url('app.js'),
                'http://localhost/static/app.deadb33f.js'
            )

    def test_static_path(self):
        app = make_app(static_url_path='/foobar')

        with app.test_request_context():
            self.assertEqual(
                asset_url('app.js'),
                'http://localhost/foobar/app.deadb33f.js'
            )

    def test_base_directory(self):
        """
        Built assets can be in a subdirectory
        """
        app = make_app(config={
            'ASSETREV_BASE_PATH': 'foobar',
        })

        with app.test_request_context():
            self.assertEqual(
                asset_url('app.js'),
                'http://localhost/static/foobar/app.deadb33f.js'
            )

    def test_base_url(self):
        """
        The url for the assets could not be part of the flask routes.
        """
        app = make_app(config={
            'ASSETREV_BASE_URL': '//cdn.myapp.com/',
        })

        with app.test_request_context():
            self.assertEqual(
                asset_url('app.js'),
                '//cdn.myapp.com/app.deadb33f.js'
            )

    def test_base_url_and_directory(self):
        """
        Completely custom url.
        """
        app = make_app(config={
            'ASSETREV_BASE_URL': '//cdn.myapp.com/',
            'ASSETREV_BASE_PATH': 'foobar',
        })

        with app.test_request_context():
            from flask.ext import assetrev

            self.assertEqual(
                assetrev.asset_url('app.js'),
                '//cdn.myapp.com/foobar/app.deadb33f.js'
            )

    def test_missing_asset(self):
        """
        What happens when an asset could not be found.
        """
        app = make_app(config={
            'ASSETREV_BASE_URL': '//cdn.myapp.com/',
            'ASSETREV_BASE_PATH': 'foobar',
        })

        with app.test_request_context():
            with self.assertRaises(asset_url.missing) as ctx:
                asset_url('missing.js')

            self.assertEqual(ctx.exception.asset_file, 'missing.js')
