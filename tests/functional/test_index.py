 
def test_index(test_client):
    """
    GIVEN the coolio app configured for testing
    WHEN the root page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200 
    assert b"Welcome to Coolio" in response.data
    
    # read_response_json = json.loads(response.data)  
    # print(read_response_json)  
    # assert len(read_response_json) == 1

def test_index_post(test_client):
    """
    GIVEN the coolio app configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Welcome to Coolio" not in response.data