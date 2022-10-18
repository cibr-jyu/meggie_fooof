from setuptools import setup

setup(
    name='meggie_fooof',
    version='0.2.1',
    description="",
    author='CIBR',
    author_email='erkka.heinila@jyu.fi',
    url='https://github.com/Teekuningas/meggie_fooof',
    license='BSD',
    packages=['meggie_fooof'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'meggie>=1.3.0',
        'fooof'
    ]
)
