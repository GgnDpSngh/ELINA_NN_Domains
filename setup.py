import subprocess
from setuptools import setup, Extension
from distutils.command.install import install as _install
from setuptools.command.build_ext import build_ext

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


gmp = Extension('libgmp',
                     sources=['elina_auxiliary/coeff_test.c', 'elina_auxiliary/elina_coeff.c','elina_auxiliary/elina_interval.c','elina_auxiliary/elina_linexpr0.c','elina_auxiliary/elina_scalar.c',  'elina_auxiliary/elina_texpr0.c', 'elina_auxiliary/elina_abstract0.c', 'elina_auxiliary/elina_dimension.c', 'elina_auxiliary/elina_lincons0.c', 'elina_auxiliary/elina_manager.c', 'elina_auxiliary/elina_tcons0.c'],
                    libraries = ['elina_auxiliary/elinaux'],
                    extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64", "-march=native", "-ffp-contract=off"],)

elinaux = Extension('libelinaux',
                     sources=['elina_auxiliary/coeff_test.c', 'elina_auxiliary/elina_coeff.c','elina_auxiliary/elina_interval.c','elina_auxiliary/elina_linexpr0.c','elina_auxiliary/elina_scalar.c',  'elina_auxiliary/elina_texpr0.c', 'elina_auxiliary/elina_abstract0.c', 'elina_auxiliary/elina_dimension.c', 'elina_auxiliary/elina_lincons0.c', 'elina_auxiliary/elina_manager.c', 'elina_auxiliary/elina_tcons0.c'],
                    libraries = ['elina_auxiliary/elinaux'],
                    extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64", "-march=native", "-ffp-contract=off"],)

elinalinearize = Extension('libelinalinearize',
                     sources=['elina_linearize/elina_coeff_arith.c', 'elina_linearize/elina_interval_arith.c', 'elina_linearize/elina_linearize_texpr.c', 'elina_linearize/elina_scalar_arith.c',
'elina_linearize/elina_generic.c', 'elina_linearize/elina_linearize.c', 'elina_linearize/elina_linexpr0_arith.c'],
                    libraries = ['elinalinearize'],
                    include_dirs = ['elina_auxiliary'],
                    extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64", "-march=native", "-ffp-contract=off", "-I../elina_auxiliary"],
                    extra_link_args=["-L../elina_auxiliary"])

elinazonotope = Extension('libzonotope',
                     include_dirs = ['elina_auxiliary', 'elina_linearize'],
                     sources=['elina_zonotope/elina_box_assign.c','elina_zonotope/elina_box_meetjoin.c', 'elina_zonotope/zonotope_internal.c', 'elina_zonotope/zonotope_representation.c', 'elina_zonotope/elina_box_constructor.c',  'elina_zonotope/elina_box_representation.c',  'elina_zonotope/zonotope_assign.c',  'elina_zonotope/zonotope_meetjoin.c',  'elina_zonotope/zonotope_resize.c', 'elina_zonotope/elina_box_internal.c', 'elina_zonotope/elina_box_resize.c', 'elina_zonotope/zonotope_constructor.c',  'elina_zonotope/zonotope_otherops.c'],
                    libraries = ['zonotope'],
                    extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64", "-march=native", "-ffp-contract=off"],
                    extra_link_args=["-L../elina_auxiliary", "-L../elina_linearize"])

zonoml = Extension('libzonoml',
                    include_dirs = ['elina_auxiliary', 'elina_linearize', 'elina_zonotope'],
                     sources=['zonoml/zonoml_fun.c', 'zonoml/zonoml_internal.c', 'zonoml/zonoml_reduced_product.c'],
                    libraries = ['zonoml'],
                    extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64", "-march=native", "-ffp-contract=off"],
                    extra_link_args=["-L../elina_auxiliary", "-L../elina_linearize", "-L../elina_zonotope"]
                    )

fppoly = Extension('libfppoly',
                     include_dirs = ['elina_auxiliary', 'elina_linearize','elina_zonotope'],
                     extra_compile_args=["-Wcast-qual", "-Wswitch", "-Wall", "-Wextra", "-Wundef", "-Wcast-align", "-Wno-unused", "-U__STRICT_ANSI__", "-fPIC", "-O3", "-DNDEBUG", "-Werror-implicit-function-declaration", "-Wbad-function-cast", "-Wstrict-prototypes", "-Wno-strict-overflow", "-std=c99", "-D_GNU_SOURCE", "-pthread", "-fno-tree-vectorize", "-m64", "-march=native", "-ffp-contract=off"],
                     sources=['fppoly/backsubstitute.c', 'fppoly/clip_approx.c', 'fppoly/expr.c', 'fppoly/leakyrelu_approx.c', 'fppoly/lstm_approx.c', 'fppoly/pool_approx.c', 'fppoly/round_approx.c' ,'fppoly/sign_approx.c', 'fppoly/batch_normalization.c', 'fppoly/compute_bounds.c', 'fppoly/fppoly.c', 'fppoly/log_approx.c', 'fppoly/parabola_approx.c', 'fppoly/relu_approx.c',  'fppoly/s_curve_approx.c'],
                    libraries = ['fppoly'],
                    extra_link_args=["-L../elina_auxiliary", "-L../elina_linearize"])
        
setup(
    name='elina_nn_py',
    version='0.0.2',    
    description='ELINA Python package for neural network certification',
    url='https://github.com/GgnDpSngh/ELINA_NN_Domains',
    author='Gagandeep Singh',
    author_email='ggnds@illinois.edu',
    license='GNU GPL3',
    install_requires=['gmpy'],
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
    #package_data={'elina_nn_py': ['libelinaux.so', 'libelinalinearize.so', 'libzonotope.so','libzonoml.so','libfppoly.so']},
    setup_requires = ['setuptools>=18.0'],
    #has_ext_modules=lambda: True,
    ext_modules=[gmp, elinaux, elinalinearize, elinazonotope, zonoml, fppoly]#[Extension('elina_auxiliary', ['elina_auxiliary/libelinaux'])]
    #Extension("elina_nn", libraries=["libelinaux.so"]),
)

