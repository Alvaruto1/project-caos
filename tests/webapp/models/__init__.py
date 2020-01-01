"""Import all the models from the project"""

import pkgutil as _pkgutil
_search_path = ['tests/webapp/models']
__all__ = [x[1] for x in _pkgutil.iter_modules(path=_search_path)]