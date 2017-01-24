import sys


def sam_ctypes(func):
    # Decorator to convert SAM ctypes
    # Written by: solarjoe

    def func_wrapper(*args):
        if sys.version_info.major > 2:

            # this syntax works in versions 2.5+
            args_conv = [a.encode('ascii') if isinstance(a, str) else a for a in args]

            rv = func(*args_conv)

            if isinstance(rv, bytes):
                # one module returns a invalid utf character, 'replace' 'ignore' 'backslashreplace'
                return rv.decode('utf-8', 'ignore')  # .decode('utf-8', 'ignore')
            else:
                return rv

        else:
            rv = func(*args)
            return rv

    return func_wrapper
