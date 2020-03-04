def authenticated(session):
    return session.get('usuario')
