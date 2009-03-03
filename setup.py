try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Orphereus',
    version="1.0.0",
    description='Powerful imageboard engine',
    author='Anoma Chan',
    #author_email='',
    url='http://orphereus.anoma.ch',
    install_requires=["Pylons>=0.9.7", "sqlalchemy>=0.5.1",
                      "mutagen>=1.15", "pil>=1.1.6",
                      "simpleparse>=2.1", "egenix-mx-base>=3.1.0",
                      "pycaptcha>=0.4", "html5lib>=0.11.0"],

    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'fc': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'fc': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = fc.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
