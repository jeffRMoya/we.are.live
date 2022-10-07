# imports the app I made and runs all the stuff in __init__.py
from my_app import create_app

app = create_app()

# only if we run this file, NOT import, will this execute
# runs flask app, debug=True auto re-runs server when changes are made
if __name__ == '__main__':
    app.run(debug=True)
