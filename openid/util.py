"""
w3cdate, strxor and random_string functions are written by Paul Crowley and distributed with this package under separate MIT license. paul@ciphergoth.org
"""

import calendar
import random
import time
import datetime
import pickle
import binascii
import sha
import hmac

from urllib import urlencode

from openid.errors import ProtocolError

# XXX: set __all__


class UTC(datetime.tzinfo):
    ZERO = datetime.timedelta(0)

    def utcoffset(self, unused_dt):
        return self.ZERO

    def tzname(self, unused_dt):
        return "UTC"

    def dst(self, unused_dt):
        return self.ZERO

utc = UTC()

def timestamp2datetime(ts):
    return datetime.datetime.fromtimestamp(ts, utc)

def datetime2timestamp(dt):
    return calendar.timegm(dt.utctimetuple())

def utc_now():
    return datetime.datetime.now(utc)

def sha1(s):
    return sha.new(s).digest()

def long2a(l):
    if l == 0:
        return '\x00'
    
    return ''.join(reversed(pickle.encode_long(l)))

def a2long(s):
    return pickle.decode_long(''.join(reversed(s)))

def w3cdate(x):
    """Represent UNIX time x as a W3C UTC timestamp"""
    dt = datetime.datetime.utcfromtimestamp(x)
    dt = dt.replace(microsecond=0)
    return dt.isoformat() + 'Z'

def w3c2datetime(x):
    return datetime.datetime(
        tzinfo=utc, *time.strptime(x, '%Y-%m-%dT%H:%M:%SZ')[:7])

def to_b64(s):
    """Represent string s as base64, omitting newlines"""
    return binascii.b2a_base64(s)[:-1]

def from_b64(s):
    return binascii.a2b_base64(s)

def kvform(d):
    "Represent dict d as newline-terminated key:value pairs"
    return ''.join(['%s:%s\n' % (k, v) for k, v in d.iteritems()])

def parsekv(d):
    d = d.strip()
    args = {}
    for line in d.split('\n'):
        pair = line.split(':', 1)
        if len(pair) != 2: continue
        k, v = pair
        args[k.strip()] = v.strip()
    return args

def strxor(aa, bb):
    return "".join([chr(ord(a) ^ ord(b)) for a, b in zip(aa, bb)])

def sign_reply(reply, key, signed_fields):
    """Sign the given fields from the reply with the specified key.
    Return signed and sig"""
    token = []
    for i in signed_fields:
        token.append((i, reply['openid.' + i]))
    
    text = ''.join(['%s:%s\n' % (k, v) for k, v in token])
    return ','.join(signed_fields), to_b64(hmac.new(key, text, sha).digest())

def append_args(url, args):
    if len(args) == 0:
        return url

    return '%s%s%s' % (url, ('?' in url) and '&' or '?', urlencode(args))

def random_string(length, srand):
    """Produce a string of length random bytes using srand as a source of
    random numbers."""
    return ''.join([chr(srand.randrange(256)) for _ in xrange(length)])



class DiffieHellman(object):
    DEFAULT_MOD = 155172898181473697471232257763715539915724801966915404479707795314057629378541917580651227423698188993727816152646631438561595825688188889951272158842675419950341258706556549803580104870537681476726513255747040765857479291291572334510643245094715007229621094194349783925984760375594985848253359305585439638443L

    DEFAULT_GEN = 2

    @classmethod
    def fromBase64(cls, p=None, g=None, srand=None):
        if p is not None:
            p = a2long(from_b64(p))
        if g is not None:
            g = a2long(from_b64(g))

        return cls(p, g, srand)
    
    def __init__(self, p=None, g=None, srand=None):
        if p is None:
            p = self.DEFAULT_MOD
        self.p = long(p)

        if g is None:
            g = self.DEFAULT_GEN
        self.g = long(g)

        if srand is None:
            srand = random

        self.x = srand.randrange(1, p - 1)

    def createKeyExchange(self):
        return pow(self.g, self.x, self.p)

    def decryptKeyExchange(self, keyEx):
        return pow(keyEx, self.x, self.p)