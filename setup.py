from setuptools import find_packages, setup

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


def get_requirements(filename):
    try:
        from pip._internal.download import PipSession
        session = PipSession()
    except ImportError:
        from pip.download import PipSession
        session = PipSession()
    except Exception:
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


def get_meta():
    mod_locals = {}

    execfile(
        "flask_assetrev/__about__.py",
        mod_locals,
        mod_locals,
    )

    return dict(
        (k, v) for k, v in mod_locals.items() if k in mod_locals["__all__"]
    )


meta = get_meta()


setup_args = dict(
    name="Flask-AssetRev",
    version=meta["version"],
    maintainer=meta["maintainer"],
    maintainer_email=meta["maintainer_email"],
    description=meta["description"],
    url=meta["url"],
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    tests_require=get_requirements("requirements_dev.txt"),
)


if __name__ == "__main__":
    setup(**setup_args)
