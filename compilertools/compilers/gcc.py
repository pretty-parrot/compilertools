# -*- coding: utf-8 -*-
"""GNU Compiler Collection"""
# https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html


from compilertools.compilers import CompilerBase as _CompilerBase

__all__ = ['Compiler']


class Compiler(_CompilerBase):
    """GNU Compiler Collection"""

    def __init__(self):
        _CompilerBase.__init__(self)

        # Options
        self['option']['fast_fpmath'] = {
            'compile': '-Ofast'}

        # API
        self['api']['openmp'] = {
            'compile': '-fopenmp',
            'link': '-fopenmp'}

        self['api']['openacc'] = {
            'compile': '-fopenacc'}

        self['api']['cilkplus'] = {
            'compile': '-fcilkplus -lcilkrts',
            'link': '-fcilkplus -lcilkrts'}

    def _compile_args_matrix(self, arch, cpu):
        """Return GCC compiler options availables for the
        specified CPU architecture.

        arch: CPU Architecture str."""
        # Generic optimisation
        args = [[self.Arg(args=['-flto', '-O3'])]]

        # Architecture specific optimisations
        if arch == 'x86_64':
            args += [
                # CPU Generic optimisations
                [self.Arg(args='-m64')],

                # CPU Instructions sets
                [self.Arg(args=['-mavx512cd', '-mavx512f'],
                          suffix='avx512',
                          import_if=('avx512f' in cpu.features and
                                     'avx512cd' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args=['-mavx2', '-mavx', '-msse4.2', '-msse4.1',
                                '-mssse3', '-msse2', '-msse'],
                          suffix='avx2',
                          import_if=('avx2' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args=['-mavx', '-msse4.2', '-msse4.1', '-mssse3',
                                '-msse2', '-msse'],
                          suffix='avx',
                          import_if=('avx' in cpu.features and
                                     cpu.os_supports_avx)),
                 self.Arg(),
                ],

                # CPU Generic vendor/brand optimisations
                [self.Arg(args='-mtune=intel',
                          suffix='intel',
                          import_if=cpu.vendor == 'GenuineIntel'),

                 self.Arg(),
                ]
            ]

        elif arch == 'x86':
            args += [
                # CPU Generic optimisations
                [self.Arg(args='-m32')],

                # CPU Instructions sets
                [self.Arg(args=['-mfpmath=sse', '-mavx2', '-mavx', '-msse4.2',
                                '-msse4.1', '-mssse3', '-msse2', '-msse'],
                          suffix='avx2',
                          import_if=('avx2' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args=['-mfpmath=sse', '-mavx', '-msse4.2',
                                '-msse4.1', '-mssse3', '-msse2', '-msse'],
                          suffix='avx',
                          import_if=('avx' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args=['-mfpmath=sse', '-msse4.2', '-msse4.1',
                                '-mssse3', '-msse2', '-msse'],
                          suffix='sse4_2',
                          import_if='sse4.2' in cpu.features),

                 self.Arg(args=['-mfpmath=sse', '-msse4.1', '-mssse3',
                                '-msse2', '-msse'],
                          suffix='sse4_1',
                          import_if='sse4.1' in cpu.features),

                 self.Arg(args=['-mfpmath=sse', '-msse4a', '-mssse3',
                                '-msse2', '-msse'],
                          suffix='sse4a',
                          import_if=('sse4a' in cpu.features and
                                     cpu.vendor == 'AuthenticAMD')),

                 self.Arg(args=['-mfpmath=sse', '-mssse3', '-msse2', '-msse'],
                          suffix='ssse3',
                          import_if='ssse3' in cpu.features),

                 self.Arg(args=['-mfpmath=sse', '-msse2', '-msse'],
                          suffix='sse2',
                          import_if='sse2' in cpu.features),

                 self.Arg(args=['-mfpmath=sse', '-msse'],
                          suffix='sse',
                          import_if='sse' in cpu.features),

                 self.Arg(args='-mfpmath=387'),
                ],

                # CPU Generic vendor/brand optimisations
                [self.Arg(args='-mtune=intel',
                          suffix='intel',
                          import_if=cpu.vendor == 'GenuineIntel'),

                 self.Arg(),
                ]
            ]

        return args

    def _compile_args_current_machine(self, arch, cpu):
        """Return auto-optimised compiler arguments for current machine"""
        # Base native optimisation
        args = ['-march=native -flto']

        # Arch specific optimizations
        if arch == 'x86':
            args.append('-m32')
            if 'sse' in cpu.features:
                args.append('-mfpmath=sse')

        elif arch == 'x86_64':
            args.append('-m64')

        return ' '.join(args)
