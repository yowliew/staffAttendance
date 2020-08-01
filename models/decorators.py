import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            flash('You need to be signed in.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function
