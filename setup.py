import subprocess
from setuptools import setup, Extension
from distutils.command.install import install as _install
from setuptools.command.build_ext import build_ext

class Build(build_ext):
     """Customized setuptools build command - builds protos on build."""
     def run(self):
         protoc_command = ["make"]
         if subprocess.call(protoc_command) != 0:
             sys.exit(-1)
         build_ext.run(self)


class install(_install):
    def run(self):
        subprocess.call(['make', 'clean', '-C', '.'])
        subprocess.call(['make', '-C', '.'])
        _install.run(self)
        
setup(
    name='ELINA_NN_Domains',
    version='0.0.1',    
    description='ELINA Python package for neural network certification',
    url='https://github.com/GgnDpSngh/ELINA_NN_Domains',
    author='Gagandeep Singh',
    author_email='ggnds@illinois.edu',
    license='GNU GPL3',
    packages=['ELINA_NN_Domains'],
    
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research/Engineering/Technology',
        'License :: OSI Approved :: GNU GPL3',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.6',
    ],
    package_dir={"python_interface": ""},
    #packages=setuptools.find_packages(where="python_interface"),
    python_requires=">=3.6",
    cmdclass={'build_ext': Build,},
    package_data={'': ['libelinaux.so', 'libelinalinearize.so', 'libelinazonotope.so', 'libzonoml.so', 'libfpppoly.so']},
    setup_requires = ['setuptools>=18.0', 'Cython'],
    has_ext_modules=lambda: True,
)

