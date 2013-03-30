from pyramid.security import (Allow, Deny, Everyone,Authenticated )

class RootFactory(object):
    __acl__ = [
                (Allow, Everyone, "view"),
                (Allow, Authenticated, "edit"),
              ] 
    def __init__(self, request):
       pass