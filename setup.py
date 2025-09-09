from setuptools import setup, find_packages

setup(
    name='ref_toolkit',
    version='1.0.0',
    description='Helios: toolkit for the Resonant Entropy Field simulations and analytics',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy', 'scipy', 'matplotlib', 'pymc', 'click'
    ],
    entry_points={
        'console_scripts': [
            'ref-fpe=ref_toolkit.cli:main',
            'ref-sim=ref_toolkit.sim.neuromorphic_diagram:main'
        ]
    },
)