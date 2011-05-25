import memcache
import collections

import telnetlib



class MCDict(collections.MutableMapping):
    __version__ = "1.01"
    def __init__(self, *args, **kwargs):
	'''pass through memcache connection params'''
        if "mcaddress" not in  kwargs:
            mcaddress = '127.0.0.1:11211'
        else:
            mcaddress = kwargs["mcaddress"]
            del kwargs["mcaddress"]
        if "debug" not in kwargs:
            debugopt = 0
        else:
            debugopt = kwargs["debug"]
            del kwargs["debug"]
        self.host, self.port = mcaddress.split(":")
	self.mc = memcache.Client([mcaddress], debug=debugopt)
        # unlike dict, this adds the keys to the memcache
        # in other words, we assume that this memcache will be used to share data between processes
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        val = self.mc.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __setitem__(self, key, val):
        self.mc.set(key, val)

    def __delitem__(self, key):
        ''' if you type   del dict[key]  then this method is called'''
        self.mc.delete(key)
 
    def __iter__(self):
        '''this iterator relies on our ability to telnet and issue stats commands'''
        self._keys = self.keys()
        self.curitm = -1 # need to incr this before accessing item
        self._len = len(self._keys) - 1 # account for strange increment style
        return self

    def next(self):
        '''this method allows use in list comrehensions etc...'''
        if self.curitm < self._len:
            self.curitm += 1
            return self._keys[self.curitm]
        else:
            raise StopIteration

    def keys(self):
        '''not available in the memcache protocol so we get it via telnet'''
	self.tn = telnetlib.Telnet(self.host, self.port)
	def wcmd(cmd):
            self.tn.write("%s\n" % cmd)
            return self.tn.read_until('END')

	def key_details():
            ' Return a list of tuples containing keys and details '
            cmd = 'stats cachedump %s 2000000'
            ids = [id.split()[1].split(":")[1] for id in wcmd("stats items").split("\r\n")  if not id.startswith("END")]
            ids = set(ids)
            #for key in [id.split()[1] for id in wcmd(cmd % id).split()]:
            #keys = [[key.split()[1] for key in 
            keys = []
            for id in ids:
                res = wcmd(cmd % id).split("\r\n")
                keys.extend([key.split()[1] for key in res if key != '' and not key.startswith("END")])
            return keys

        return key_details()
        #return [key[0] for key in mem.key_details(sort=None)]

    def __len__(self):
        s = self.mc.get_stats()
	return s["items"]

    def __repr__(self):
        dictrepr = dict.__repr__(dict(self))
        return '%s(%s)' % (MCDict, dictrepr)

    def update(self, *args, **kwargs):
        '''we have to overide this because it does not use __setitem___'''
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

    def flush_all(self):
        '''monkey patch in this useful memcache method to clear a dict'''
        self.mc.flush_all() # take advantage of the memcache object inside MCDict
        # this has the disadvantage of not fully deleting the keys so you
        # will have to make your code check for None values

if __name__ == "__main__":
    import unittest
    class testmc(unittest.TestCase):
        '''test the MCDict class'''

        def setUp(self):
            self.mc = MCDict()
            self.mc.flush_all()
            for k in self.mc.keys(): # we have to do this to make all the keys go away
                self.mc.mc.delete(k) # use memcached's delete method

        def failOnKeyError(self):
            junk = self.mc["AKeyThatDoesNotExist"]

        def testNoKey(self):
            self.assertRaises(KeyError, self.failOnKeyError)
            #self.failOnKeyError()

        def testSetGet(self):
            aKey = "fred"
            aVal = "Some data to be stored"
            self.mc[aKey] = aVal
            self.assertEqual(self.mc[aKey], aVal)

        def testIter(self):
            self.mc["akey"] = "junk"
            self.mc["fred"] = "junk"
            self.mc["blue"] = "junk"
            self.assertEqual(sorted([k for k in self.mc]), ["akey","blue","fred"])

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(testmc))
        return suite

    unittest.TextTestRunner(verbosity=2).run(suite())
    print MCDict().keys()
    print MCDict().items()
