def get_session_id(request):
    session_id = request.session.session_key

    if session_id is None:
        request.session.create()
        session_id = request.session.session_key

    return session_id
