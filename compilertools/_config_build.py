# -*- coding: utf-8 -*-
"""Extra configuration for build"""

# Default configuration
CONFIG_BUILD = {
    # Disable optimisations
    'disabled': False,

    # Compile optimized for current machine only
    # (If not compile for a cluster of possibles machines)
    'current_machine': False,

    # Enable compilers options
    'option': {
        # Enable Fast floating point math
        'fast_fpmath': False
        },

    # Specific API are auto-enabled when compiling and linking
    # if following preprocessors are detected in source files
    'api': {
        # openMP
        'openmp': {
            'c':'#pragma omp ',
            'fortran': ('!$omp ', 'c$omp ', '*$omp ')},
        # OpenACC
        'openacc': {
            'c': '#pragma acc ',
            'fortran': ('!$acc ', 'c$acc ', '*$acc ')},
        # Intel Cilk Plus
        'cilkplus': {
            'c': '#pragma simd ',
            'fortran': '!dir$ simd '}
            },

    # Sources files extensions for code analysis
    'extensions': {
        # C/C++ sources files extensions
        'c': ('.c', '.cpp', '.cxx', '.cc', '.c++', '.cp'),
        # Fortran sources files extensions
        'fortran': ('.f', '.for', '.f90', '.f95', '.f03', '.f08', '.f15')
        }
    }
