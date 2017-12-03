# -*- coding: utf-8 -*-
"""Tests for compilers core"""

def tests_get_compiler():
    """Test get_compiler"""
    from os import listdir
    from os.path import splitext, dirname
    from compilertools._config import CONFIG
    from compilertools.compilers import CompilerBase, _core
    from compilertools.compilers._core import get_compiler
    from distutils.ccompiler import get_default_compiler

    # Return compiler in parameter
    compiler = CompilerBase()
    assert get_compiler(compiler) is compiler

    # Return default compiler
    name = get_default_compiler()
    assert (get_compiler().__class__.__module__ ==
            'compilertools.compilers.%s' %
            CONFIG['compiler_alias'].get(name, name))

    # Return compiler by name
    # with all file in "compilertools.compilers"
    for file in listdir(dirname(_core.__file__)):
        if file.startswith('_'):
            continue
        name = splitext(file)[0]
        assert (get_compiler(name).__class__.__module__ ==
                'compilertools.compilers.%s' % name)

    # Test aliases
    for name in CONFIG['compiler_alias']:
        assert (get_compiler(name).__class__.__module__ ==
                'compilertools.compilers.%s' %
                CONFIG['compiler_alias'][name])


def tests_compiler_base():
    """Test CompilerBase"""
    from os import listdir
    from os.path import splitext, dirname
    from collections import OrderedDict
    from compilertools.processors import _core
    from compilertools.processors._core import get_processor
    from compilertools.compilers import CompilerBase

    # Initialise base compiler
    compiler = CompilerBase()

    # Initialise compiler subclass
    class Compiler(CompilerBase):
        """Dummy Compiler"""

        def compile_args_matrix(self, arch):
            """Return test args matrix"""
            return [

                [self.Arg(args=['--generic'])],

                [self.Arg(args='--inst1',
                          suffix='inst1'),

                 self.Arg(args='--inst2',
                          suffix='inst2',
                          # Not compatible with current compiler
                          build_if=False),

                 self.Arg(),
                ],

                # Compatible only with a specific arch
                [self.Arg(args='--arch1',
                          suffix='arch1',
                          import_if=(arch == 'arch1')),

                 self.Arg(args='--arch2',
                          suffix='arch2',
                          import_if=(arch == 'arch2')),
                ]
            ]

    sub_compiler = Compiler()

    class Compiler2(CompilerBase):
        """Dummy Compiler"""

        def compile_args_matrix(self, arch):
            """Return test args matrix"""
            return [

                [self.Arg(args=['--generic'])],

                [self.Arg(args='--inst1',
                          suffix='inst1'),

                 self.Arg(args='--inst2',
                          suffix='inst2',
                          # Not compatible with current compiler
                          build_if=False),

                 self.Arg(),
                ],

                # Compatible only with a specific arch
                [self.Arg(args='--arch1',
                          suffix='arch1',
                          import_if=(True)),

                 self.Arg(args='--arch2',
                          suffix='arch2',
                          import_if=(False)),
                ]
            ]

    sub_compiler2 = Compiler2()

    # Initialise args results
    excepted = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
        ('inst2-arch1', ['--generic', '--inst2', '--arch1']),
        ('inst2-arch2', ['--generic', '--inst2', '--arch2']),
        ('arch1', ['--generic', '--arch1']),
        ('arch2', ['--generic', '--arch2'])])

    excepted_currentmachine = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst2-arch1', ['--generic', '--inst2', '--arch1']),
        ('arch1', ['--generic', '--arch1'])])

    excepted_currentcompiler = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
        ('arch1', ['--generic', '--arch1']),
        ('arch2', ['--generic', '--arch2'])])

    # Test get_arch_and_cpu
    for file in listdir(dirname(_core.__file__)):
        if file.startswith('_'):
            continue
        arch = splitext(file)[0]
        assert compiler.get_arch_and_cpu(arch) == arch
        assert compiler._cpu == get_processor(arch)

    # Test compile_args_matrix: Empty because abstract
    assert compiler.compile_args_matrix('arch') == []

    # Test _order_args_matrix
    matrix = sub_compiler.compile_args_matrix('arch1')
    assert CompilerBase._order_args_matrix(matrix) == excepted
    assert CompilerBase._order_args_matrix(
        matrix, current_machine=True) == excepted_currentmachine
    assert CompilerBase._order_args_matrix(
        matrix, current_compiler=True) == excepted_currentcompiler

    # Test compile_args
    assert sub_compiler.compile_args(arch='arch1') == excepted
    assert sub_compiler.compile_args(
        arch='arch1', current_machine=True) == excepted_currentmachine
    assert sub_compiler.compile_args(
        arch='arch1', current_compiler=True) == excepted_currentcompiler

    # Test compile_args_current_machine
    assert (sub_compiler2.compile_args_current_machine() ==
            excepted['inst1-arch1'])
    assert (sub_compiler.compile_args_current_machine() == [])

    # Test Properties
    assert compiler.version == 0.0
    compiler['version'] = 9.9
    assert compiler.version == 9.9

    # Test support check
    assert compiler.support_api('api') is False
    compiler['api']['api'] = {'compiler': ''}
    assert compiler.support_api('api') is True

    assert compiler.support_option('option') is False
    compiler['option']['option'] = {'compiler': ''}
    assert compiler.support_option('option') is True
