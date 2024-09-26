from setuptools import find_packages, setup

package_name = 'my_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='looubuntu',
    maintainer_email='looubuntu@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
	entry_points={
		'console_scripts': [
            # 'service = my_pkg.service_member_function:main',
            # 'client = my_pkg.client_member_function:main',
            # 'service = my_pkg.service:main',
            'control = my_pkg.a_to_b_ver2:main',
		],
	},
)
