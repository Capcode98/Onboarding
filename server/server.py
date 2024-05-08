from app import app, auth, socketIo

if __name__ == "__main__":
    socketIo.run(app)
