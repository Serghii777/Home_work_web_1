from setuptools import setup, find_namespace_packages

setup (
    name='Personal_Helper',
      version='0.0.1',
      description='Very useful code',
      
      author='Py-Power',
      author_email='dmytro.ost1@gmail.com',
      license='MIT',
      classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['greeting=Personal_Helper.main:greeting']}
)
      
      
   

