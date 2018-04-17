from setuptools import find_packages
from setuptools import setup

setup(
    name='libnmea_navsat_driver',
    version='0.4.0',
    packages=find_packages(exclude=['test']),
    zip_safe=True,
    author='Eric Perko',
    author_email='eric@ericperko.com',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description=(
        'Python nodes which read GPS data from serial and publish them.'
    ),
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nmea_serial_driver = libnmea_navsat_driver.entry_points.nmea_serial_driver:nmea_serial_driver'
        ],
    },
)
        
