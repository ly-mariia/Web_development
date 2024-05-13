#/bin/bash

pip install pytest pytest-cov

pip install locust

pytest test.py

coverage run -m pytest test.py # 1
coverage report -m # 2

coverage html

locust -f locustfile.py --host=http://localhost:8000



