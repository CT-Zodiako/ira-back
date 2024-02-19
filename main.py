import os
from IRA import create_app


app = create_app()

if __name__ == '__main__':
    app.run(port=os.environ.get('PORT'), debug=os.environ.get('DEBUG'))
