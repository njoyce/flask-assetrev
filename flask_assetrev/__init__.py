import os.path

from flask import json, url_for, current_app

from . import _pkg_meta

__version__ = _pkg_meta.version
__version_info__ = _pkg_meta.version_info


__all__ = [
    'AssetRev',
    'AssetMissingError',
    'asset_url',
]


class AssetMissingError(Exception):
    """
    Raised if attempting to match a source asset fails.

    :ivar asset_file: The file that was attempted to be found.
    """

    def __init__(self, asset_file):
        self.asset_file = asset_file

        super(AssetMissingError, self).__init__(
            'Failed to find asset file{!r}'.format(asset_file)
        )


class AssetRev(object):
    """
    Maintains a map of source -> hashed assets by name.

    There are two usage modes which work very similarly.  One is binding
    the instance to a very specific Flask application::

        app = Flask(__name__)
        asset_rev = AssetRev(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        asset_rev = AssetRev()

        def create_app():
            app = Flask(__name__)
            asset_rev.init_app(app)

            return app

    :ivar app: The bound ``Flask`` application.
    :ivar _assets: The loaded manifest contents.
    """

    def __init__(self, app=None):
        self.app = None
        self._assets = None

        if app:
            self.init_app(app)

    @property
    def manifest_file(self):
        """
        The location of the manifest file - relative to the app_root.

        The file is a json dict of the name of the source asset -> the compiled
        version. Example::

            {
              "app.js": "app.deadb33f.js"
            }
        """
        filename = self.app.config['ASSETREV_MANIFEST_FILE']

        return os.path.join(self.app.root_path, filename)

    @property
    def base_path(self):
        """
        The directory within which to find the compiled assets in the app's
        static_folder.
        """
        return self.app.config['ASSETREV_BASE_PATH']

    @property
    def base_url(self):
        """
        The url to find the compiled assets. By default the same host will be
        used. This allows the assets to be in a completely different domain by
        the app to be able to refer to them anyway. Pretty cool! :)
        """
        return self.app.config['ASSETREV_BASE_URL']

    @property
    def reload(self):
        """
        Whether to reload the manifest at the start of every request. This is
        useful for debugging when using an external build system.
        """
        return self.app.config['ASSETREV_RELOAD']

    def init_app(self, app):
        app.config.setdefault('ASSETREV_MANIFEST_FILE', 'asset-manifest.json')
        app.config.setdefault('ASSETREV_BASE_URL', None)
        app.config.setdefault('ASSETREV_BASE_PATH', None)
        app.config.setdefault('ASSETREV_RELOAD', app.debug)

        app.extensions['assetrev'] = self

        app.context_processor(jinja_context)

        self.app = app

        self.load_assets()

    def load_assets(self):
        """
        Load the assets from the manifest file.
        """
        with open(self.manifest_file, 'rb') as fp:
            self._assets = json.loads(fp.read())

        return self._assets

    def get_asset_file(self, asset):
        if self.reload:
            self.load_assets()

        asset_file = self._assets.get(asset, None)

        if not asset_file:
            raise AssetMissingError(asset)

        return asset_file

    def get_asset_url(self, asset):
        asset_file = self.get_asset_file(asset)

        if self.base_path:
            asset_file = os.path.join(self.base_path, asset_file)

        if self.base_url:
            return self.base_url + asset_file

        return url_for(
            'static',
            filename=asset_file,
            _external=True
        )


def get_extension(app=None):
    """
    Gets the :ref:`AssetRev` extension for the application.
    """
    app = app or current_app

    assetrev = app.extensions.get('assetrev', None)

    if not assetrev:
        raise AssertionError(
            'The assetrev extension was not registered to the current '
            'application.  Please make sure to call init_app() first.'
        )

    return assetrev


def jinja_context():
    """
    The context for the jinja templates.
    """
    return {
        'asset_url': asset_url,
    }


def asset_url(asset_file):
    asset_rev = get_extension()

    return asset_rev.get_asset_url(asset_file)

asset_url.missing = AssetMissingError
