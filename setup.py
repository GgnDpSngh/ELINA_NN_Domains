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
    name='elina_nn_py',
    version='0.0.2',    
    description='ELINA Python package for neural network certification',
    url='https://github.com/GgnDpSngh/ELINA_NN_Domains',
    author='Gagandeep Singh',
    author_email='ggnds@illinois.edu',
    license='GNU GPL3',
    
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research/Engineering/Technology',
        'License :: OSI Approved :: GNU GPL3',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.6',
    ],
    packages=["elina_auxiliary", "elina_linearize", "elina_zonotope", "zonoml", "fppoly", "elina_nn_py"],
    package_dir={"elina_auxiliary": "elina_auxiliary", "elina_linearize": "elina_linearize", "elina_zonotope": "elina_zonotope", "zonoml": "zonoml", "fppoly": "fppoly", "elina_nn_py":"elina_nn_py"},
    python_requires=">=3.6",
    cmdclass={'build_ext': Build, 'install': install},
    package_data={'elina_auxiliary': ['libelinaux.so'], 'elina_linearize': ['libelinalinearize.so'], 'elina_zonotope': ['libzonotope.so'], 'zonoml': ['libzonoml.so'], 'fppoly': ['libfppoly.so'], "elina_nn_py": ["elina_nn_py"]},
    setup_requires = ['setuptools>=18.0', 'Cython'],
    has_ext_modules=lambda: True,
)

