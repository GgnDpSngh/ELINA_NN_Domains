import subprocess
from setuptools import setup, Extension
from distutils.command.install import install as _install
from setuptools.command.build_ext import build_ext

from distutils.command.install_lib import install_lib as _install_lib
import re
import os

def batch_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
    '''Same as os.rename, but returns the renaming result.'''
    os.rename(src, dst,
              src_dir_fd=src_dir_fd,
              dst_dir_fd=dst_dir_fd)
    return dst

class _CommandInstallCythonized(_install_lib):
    def __init__(self, *args, **kwargs):
        _install_lib.__init__(self, *args, **kwargs)

    def install(self):
        # let the distutils' install_lib do the hard work
        outfiles = _install_lib.install(self)
        # batch rename the outfiles:
        # for each file, match string between
        # second last and last dot and trim it
        matcher = re.compile('\.([^.]+)\.so$')
        return [batch_rename(file, re.sub(matcher, '.so', file))
                for file in outfiles]

class Build(build_ext):
     """Customized setuptools build command - builds protos on build."""
     def run(self):
         subprocess.call(["./configure"])
         protoc_command = ["make"]
         if subprocess.call(protoc_command) != 0:
             sys.exit(-1)
         build_ext.run(self)


class install(_install):
    def run(self):
        subprocess.call(["./configure"])
        #subprocess.call(['make', 'clean'])
        subprocess.call(['make'])
        #subprocess.call(['make', 'install', '-C', '.'])
        #protoc_command = ["make"]
        #if subprocess.call(protoc_command) != 0:
        #    sys.exit(-1)
        _install.run(self)





fppoly = Extension('libfppoly',
                     
                     extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64",  "-ffp-contract=off"],
                     sources=['fppoly/backsubstitute.c', 'fppoly/clip_approx.c', 'fppoly/expr.c', 'fppoly/leakyrelu_approx.c', 'fppoly/lstm_approx.c', 'fppoly/pool_approx.c', 'fppoly/round_approx.c' ,'fppoly/sign_approx.c', 'fppoly/batch_normalization.c', 'fppoly/compute_bounds.c', 'fppoly/fppoly.c', 'fppoly/log_approx.c', 'fppoly/parabola_approx.c', 'fppoly/relu_approx.c',  'fppoly/s_curve_approx.c','fppoly/elina_coeff.c','fppoly/elina_interval.c','fppoly/elina_linexpr0.c','fppoly/elina_scalar.c',  'fppoly/elina_texpr0.c', 'fppoly/elina_abstract0.c', 'fppoly/elina_dimension.c', 'fppoly/elina_lincons0.c', 'fppoly/elina_manager.c', 'fppoly/elina_tcons0.c'],
                    #libraries = ['fppoly'],
                    )
        
setup(
    name='elina_nn_py',
    version='0.0.2',    
    description='ELINA Python package for neural network certification',
    url='https://github.com/GgnDpSngh/ELINA_NN_Domains',
    author='Gagandeep Singh',
    author_email='ggnds@illinois.edu',
    license='GNU GPL3',
    #install_requires=['gmpy'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research/Engineering/Technology',
        'License :: OSI Approved :: GNU GPL3',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.6',
    ],
    packages=["elina_nn_py"],
    #package_dir={"elina_nn_py":"elina_nn_py"},
    python_requires=">=3.6",
    #cmdclass={'install': install},
    cmdclass={
        'install_lib': _CommandInstallCythonized,
    },
    #package_data={'elina_nn_py': ['libelinaux.so', 'libelinalinearize.so', 'libzonotope.so','libzonoml.so','libfppoly.so']},
    setup_requires = ['setuptools>=18.0'],
    #has_ext_modules=lambda: True,
    ext_modules=[fppoly]#[Extension('elina_auxiliary', ['elina_auxiliary/libelinaux'])]
    #Extension("elina_nn", libraries=["libelinaux.so"]),
)

