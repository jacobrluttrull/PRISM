from prism.main import app


def test_routes_registered():
    paths = {route.path for route in app.routes}
    assert "/" in paths
    assert "/projects/new" in paths
    assert "/projects/{project_id}" in paths


def test_project_create_route_accepts_post():
    route_methods = {
        (route.path, method)
        for route in app.routes
        for method in getattr(route, "methods", [])
    }
    assert ("/projects/new", "POST") in route_methods
