import importlib.util
from distutils.core import Extension
from distutils.core import Distribution


def build(ext_modules: list[Extension], **ext_args):
    dist = Distribution({'ext_modules': ext_modules})
    cmd_obj = dist.get_command_obj('build')
    for k, v in ext_args.items(): setattr(cmd_obj, k, v)
    cmd_obj.run()
    build_ext_obj = dist.get_command_obj('build_ext')
    return [build_ext_obj.get_ext_fullpath(e.name) for e in ext_modules]


def _import_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_with_import(ext_modules: list[Extension], **ext_args):
    return [_import_by_path(e.name, p) for e, p in zip(ext_modules, build(ext_modules, **ext_args))]
