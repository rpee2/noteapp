from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True
    )  # everytime we make changes to the code, it will automatically rerun the web server
