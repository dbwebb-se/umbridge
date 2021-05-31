"""
Test handlers for request errors, app/errors/handlers
"""


def test_404(client):
    """
    Test that custom 404 page is shown when non existing route is entered.
    """
    response = client.get('/non_existing_route')
    assert response.status_code == 404
    assert b"404 Not Found: The requested URL was not found on the server." in response.data
