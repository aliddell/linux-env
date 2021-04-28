from setuptools import setup

setup(
    name='linux-env',
    version='0.1.0',
    packages=['utils', 'shell_tools'],
    url='https://github.com/aliddell/linux-env',
    license='MIT',
    author='Alan Liddell',
    author_email='alan.c.liddell@gmail.com',
    description='Some Linux utilities for a portable environment',
    install_requires=[
        'Click',
    ],
    entry_points='''
            [console_scripts]
            update-julia = shell_tools.julia_installer:update
        ''',
)
