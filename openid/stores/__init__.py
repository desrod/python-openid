class OpenIDStore(object):
    """
    This is the interface for the store objects the OpenID library
    uses.  It is a single class that provides all of the persistence
    mechanisms that the OpenID library needs, for both servers and
    consumers.


    @cvar AUTH_KEY_LEN: The length of the auth key that should be
        returned by the C{L{getAuthKey}} method.
    """

    AUTH_KEY_LEN = 20

    def storeAssociation(self, server_url, association):
        """
        This method puts a C{L{Association}} object into storage,
        retrievable by server URL and handle.

        @param server_url: The URL of the identity server that this
            association is with.

        @type server_url: C{str}

        @param association: The C{L{Association}} to store.

        @type association: C{L{Association}}
        """
        raise NotImplementedError
    

    def getAssociation(self, server_url, handle=None):
        """
        This method returns a C{L{Association}} object from storage
        that matches the server_url and handle. It returns C{None} if
        no such association is found or if the matching association is
        expired. If no handle is supplied, the store should return
        the association with the latest expiration time for this
        server URL, but may return any association.

        This method is allowed (and encouraged) to garbage collect
        expired associations when found. This method should not return
        expired associations, although it is not an error to do so.


        @param server_url: The URL of the identity server to get the
            association for.

        @type server_url: C{str}

        @param handle: This is the handle of the association to get.
            If there isn't an association found that matches both the
            given URL and handle, then None is returned.

        @type handle: C{str} or C{NoneType}

        @return: The C{L{Association}} for the given identity
            server.

        @rtype: C{L{Association}} or C{None}
        """
        raise NotImplementedError

    def removeAssociation(self, server_url, handle):
        """
        This method removes the matching association if it's found,
        and returns whether the association was removed or not.


        @param server_url: The URL of the identity server the
            association to remove belongs to.

        @type server_url: C{str}


        @param handle: This is the handle of the association to
            remove.  If there isn't an association found that matches
            both the given URL and handle, then there was no matching
            handle found.

        @type handle: C{str}


        @return: Returns whether or not the given association existed.

        @rtype: C{bool}
        """
        raise NotImplementedError


    def storeNonce(self, nonce):
        """
        Stores a nonce.  This is used to prevent replay attacks.


        @param nonce: The nonce to store.

        @type nonce: C{str}
        """
        raise NotImplementedError

    def useNonce(self, nonce):
        """
        This method is called when the library is attempting to use a
        nonce.  If the nonce is in the store, this method removes it
        and returns True.  Otherwise it returns False.

        This method is allowed and encouraged to treat nonces older
        than some period (a very conservative window would be 6 hours,
        for example) as no longer existing, and return False and
        remove them.


        @param nonce: The nonce to use.

        @type nonce: C{str}


        @return: C{True} if the nonce existed, C{False} if it didn't.

        @rtype: C{bool}
        """
        raise NotImplementedError

    def getAuthKey(self):
        """
        This method returns a key used to sign the tokens, to
        ensure that they haven't been tampered with in transit.  It
        should return the same key every time it is called.  The key
        returned should be C{L{AUTH_KEY_LEN}} bytes long.

        @return: The key.  It should be C{L{AUTH_KEY_LEN}} bytes in
            length, and use the full range of byte values.  That is,
            it should be treated as a lump of binary data stored in a
            C{str}.

        @rtype: C{str}
        """
        raise NotImplementedError

    def isDumb(self):
        """
        This method must return C{True} if the store is a
        dumb-mode-style store.  Unlike all other methods in this
        class, this one provides a default implementation, which
        returns C{False}.

        In general, any custom subclass of C{L{OpenIDStore}} won't
        override this method, as custom subclasses are only likely to
        be created when the store is fully functional.

        @return: C{True} if the store works fully, C{False} if the
           consumer will have to use dumb mode to use this store.

        @rtype: C{bool}
        """
        return False