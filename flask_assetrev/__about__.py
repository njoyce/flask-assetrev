__all__ = [
    "description",
    "maintainer",
    "maintainer_email",
    "url",
    "version_info",
    "version",
]

version_info = (1, 0, 3)
version = ".".join(map(str, version_info))

maintainer = "Nick Joyce"
maintainer_email = "nick.joyce@realkinetic.com"

description = """
Flask-AssetRev is a Flask extension which adds support for mapping pre-built,
content hashed static assets from the source form to the hashed version at
runtime.
""".strip()

url = "https://github.com/njoyce/flask-assetrev"
