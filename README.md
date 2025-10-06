# Project setup:
1. Create Virtual Environment:
    On Windows: python -m venv venv
    On Linux: python3 -m venv venv
    On MAC: python3 -m venv venv
2. Run Virtual Environment:
    On Windows: .\venv\Scripts\activate
    On Linux: source ./venv/bin/activate
    On MAC: source ./venv/bin/activate
3. Install pip requirements:
    pip install -r requirements.txt
4. Create .env file in root and add following details in env (Ask your team members for exact values. Don't share that with anyone. It's used for database access)
5. Deactivate virtual environment (It runs without deactivating too. Need more information on this behaviour):
    deactivate
6. Run Project Locally:
    uvicorn app:app --reload --host 127.0.0.1 --port 5000
    Note: For server deployment, change host to 0.0.0.0 and port to 8000(Needs Verification)
7. Optional:
    Sometimes, you need to also install pip packages on your local system outside venv. In that case, follow step 5 and then step 3 and then step 6.

# Quick Setup on Linux:
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
deactivate

# Debug Configuration: ./venv/launch.json
{
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app:app",
                "--host",
                "localhost",
                "--port",
                "5004",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}

