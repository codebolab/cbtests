from setuptools import setup, find_packages

setup(name='cbtests',
      version='0.2',
      description='Simple tests for json api testing',
      url='https://github.com/codebolab/cbtests',
      author='code.bo',
      author_email='contact@josezambrana.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      package_data={'cbtests': ['fixtures/*.json']},
      zip_safe=False)
