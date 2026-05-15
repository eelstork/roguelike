import requests
import multiprocessing
import time
import pytest
from server import app

# Need to run server in background to test it
def run_server():
    app.run(port=5001)

@pytest.fixture(scope="module")
def server():
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(1) # Give it time to start
    yield
    p.terminate()

def test_action_bad_request(server):
    # Test 1: No body
    res = requests.post("http://localhost:5001/action")
    assert res.status_code == 400
    assert "error" in res.json()

    # Test 2: Invalid JSON body
    res = requests.post("http://localhost:5001/action", data="not json", headers={"Content-Type": "application/json"})
    assert res.status_code == 400
    assert "error" in res.json()

    # Test 3: Valid JSON but missing "action" key
    res = requests.post("http://localhost:5001/action", json={"something": "else"})
    assert res.status_code == 200 # Should still work as it just skips step

def test_action_success(server):
    res = requests.post("http://localhost:5001/action", json={"action": "right"})
    assert res.status_code == 200
    assert "player_pos" in res.json()

def test_health(server):
    res = requests.get("http://localhost:5001/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
