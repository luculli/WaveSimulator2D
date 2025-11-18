from setuptools import setup, find_packages

setup(
    name='wave-sim2d',
    version='0.1.0',
    description='A lightweight 2D wave simulator running on the GPU using CuPy',
    author='0x23',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'opencv-python',
        'matplotlib',
        'cupy',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
)
