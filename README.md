# mcdict

Python class to access a memcache as if it was a dict. This implementation includes the keys() method.
All the memcache limitations are preserved, e.g. keys must be strings no longer than 250 bytes.

## Usage

Basic usage:

    import mcdict
    mc = mcdict.MCDict()

By default, it connects to localhost on port 11211. If you need to specify a host and/or port:

    mc = mcdict.MCDict('127.0.0.1', '5211')

Access the underlying memcache Client object (note second mc)

    >>> mc.mc.stats()
    {'accepting_conns': '1',
     'auth_cmds': '0',
     'auth_errors': '0',
     ... }

Retrieve a list of keys currently in use:
(note that this will cause big memcaches to block until it completes and this won't provide a complete
list of keys on very big memcaches)

    >>> mc.keys()
    ['mummy',
     'daddy',
     'masha',
     ... ]

## Installation

    pip install 'git+git://github.com/wavetossed/mcdict.git'

## License

mcdict is released under the [MIT license](http://creativecommons.org/licenses/MIT/).
