from start import create_app

if __name__ == "__main__":
    from settings import PROD
    app = create_app(PROD)
    app.run('0.0.0.0')
else:
    from settings import PROD
    app = create_app(PROD)
