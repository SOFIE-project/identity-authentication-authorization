import pytest

@pytest.fixture(autouse=True, scope="session")
def IAAComponent():
    import subprocess
    import time
    p1 = subprocess.Popen(['python3', 'IAA/iaa.py'])
    time.sleep(5) #Otherwise the server is not ready when tests start
    yield
    p1.terminate()

@pytest.fixture(autouse=True, scope="session")
def HTTPResource():
    import subprocess
    import time
    p1 = subprocess.Popen(['python3', 'tests/http_server.py'])
    time.sleep(5) #Otherwise the server is not ready when tests start
    yield
    p1.terminate()

