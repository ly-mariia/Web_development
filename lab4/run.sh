#/bin/bash

pip install pytest pytest-cov

pip install locust

pytest test.py

coverage report -m

locust -f locustfile.py --host=http://localhost:8000



