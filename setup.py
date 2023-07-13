from setuptools import setup, find_packages

setup(
    name='aiy-projects-python',
    version='1.4',
    description='AIY Python API',
    long_description='A set of Python APIs designed for the AIY Voice Kit and AIY Vision Kit, which help you build intelligent systems that can understand what they hear and see.',
    author='AIY Team',
    author_email='support-aiyprojects@google.com',
    url="https://aiyprojects.withgoogle.com/",
    project_urls={
        'GitHub: issues': 'https://github.com/viraniac/aiyprojects-raspbian/issues',
        'GitHub: repo': 'https://github.com/viraniac/aiyprojects-raspbian',
    },
    license='Apache 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'gpiozero',
        'protobuf>=3.6.1',
        'picamera',
        'Pillow',
        'RPi.GPIO',
    ],
    python_requires='>=3.5.3',
)
