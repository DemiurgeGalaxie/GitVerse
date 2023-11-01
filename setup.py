from setuptools import setup, find_packages

setup(
    name="GitVerse",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # liste des dépendances
    ],
    entry_points={
        'console_scripts': [
            'gitv=gitverse.gitv:main',  # le nom du module devrait aussi être adapté si nécessaire
        ],
    },
    # autres métadonnées, comme auteurs, emails, description, etc.
)
