from setuptools import setup

setup(
    name='py3samsdk',
    version='0.1.0',
    author='Stephen J. Schneider',
    author_email='stesch@alumni.stanford.edu',
    packages=['py3samsdk'],
    package_dir={'py3samsdk': 'py3samsdk'},
    url='https://github.com/sjschneider/py3samsdk/',
    license='GPLv3',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords='pvwatts nrel sam',
    description="Python 3 wrapper for NREL's System Advisor Model SDK.",
    install_requires=["numpy >= 1.9", ],
)
