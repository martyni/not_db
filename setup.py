from setuptools import setup
from pip.req import parse_requirements
from Not_Db.server import main

install_reqs = parse_requirements('requirements.txt', session=False)

reqs = [ str(i.req) for i in install_reqs ]

setup(name='app',
      version="v0.0.1",
      description='simple s3 storage rest api',
      url='http://github.com/martyni/not_db',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      install_requires=reqs,
      packages=['Not_Db'],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['not_db=Not_Db.server:main'],
                  },
      include_package_data=True
      )
