from portfolio.core import bp


@bp.route('/')
def hello_world():
    return 'Hello World!'
