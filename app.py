from application import create_app,Base
import uvicorn

app = create_app()


if __name__ == "__main__":
    # print("app is sstarted")
    uvicorn.run(app, host="0.0.0.0", port=5000)