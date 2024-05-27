def _load_pkgs():
    import pkgutil, os, importlib

    for i, mod in enumerate(pkgutil.iter_modules([os.path.dirname(__file__)])):
        importlib.import_module(f'{__name__}.{mod.name}')


_load_pkgs()
