import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if 'sdist' in sys.argv:
    os.system('./admin/makedoc')

if not sys.version_info[0] == 2:
    sys.exit("Sorry, Python 3 is not supported. Please use python3-openid")

version = '[library version:2.2.5]'[17:-1]

setup(
    name='python-openid',
    version=version,
    python_requires=">2.6.*,<3.0.*",
    description='OpenID support for servers and consumers.',
    long_description='''This is a set of Python packages to support use of
the OpenID decentralized identity system in your application.  Want to enable
single sign-on for your web site?  Use the openid.consumer package.  Want to
run your own OpenID server? Check out openid.server.  Includes example code
and support for a variety of storage back-ends.''',
    url='http://github.com/openid/python-openid',
    packages=['openid',
              'openid.consumer',
              'openid.server',
              'openid.store',
              'openid.yadis',
              'openid.extensions',
              'openid.extensions.draft',
              ],
    # license specified by classifier.
    # license=getLicense(),
    author='JanRain',
    author_email='openid@janrain.com',
    download_url='http://github.com/openid/python-openid/tarball/%s' % (version,),
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Systems Administration :: Authentication/Directory",
    ],
    )
