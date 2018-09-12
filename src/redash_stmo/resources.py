from redash.handlers import api

def add_resource(app, resource, endpoint):
    """
    After api.init_app() is called, api.app should be set by Flask (but it's not) so that
    further calls to add_resource() are handled immediately for the given app.
    """
    api.app = app
    api.add_org_resource(resource, endpoint)
