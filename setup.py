from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'packaging',
    'reverse_geocoder',
    'fast_json',
    'boto3',
    'backoff',
    'haversine',
    'osmnx',
    'scikit-learn',
    'requests',
    'geopandas'
)

setup(
    name='via',
    version='0.0.1',
    python_requires='>=3.6',
    description='Bike',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/via',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'pull_journeys = via.bin.pull_journeys:main',
            'plot_journeys = via.bin.plot_journeys:main',
            'road_coverage = via.bin.road_coverage:main',
            'condition_by_street = via.bin.condition_by_street:main'
        ]
    }
)
