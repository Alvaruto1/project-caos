"""Import all the controllers from the project"""

import pkgutil as _pkgutil
_search_path = ['tests/webapp/controllers']
__all__ = [x[1] for x in _pkgutil.iter_modules(path=_search_path)]