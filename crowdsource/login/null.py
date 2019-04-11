
def null_login(handler, user):
    '''
    handler: instance of crowdsource.handlers.ServerHandler
    user: user token from secret cookie
    returns: crowdsource.Structs.ClientStruct or None
    '''
    return handler._clients.get(user, None)
