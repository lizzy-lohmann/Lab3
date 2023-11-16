from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__, static_folder='templates/static')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Lab3']  # Use 'Lab3' as the database name
collection = db['users']  # Use 'users' as the collection name

# Initialize a dictionary to store comments for each page
page_comments = {
    'justin_schumacher': [],
    'lizzy_lohmann': [],
    'brenna_gogel': [],
    'chase_dittmer': [],
}


@app.route('/')
def index():
    # Retrieve data from MongoDB
    data = collection.find()
    return render_template('index.html', data=data)


@app.route('/justin_schumacher')
def justin_schumacher():
    comments = page_comments.get('justin_schumacher', [])
    return render_template('JustinSchumacher.html', comments=comments)


@app.route('/lizzy_lohmann')
def lizzy_lohmann():
    comments = page_comments.get('lizzy_lohmann', [])
    return render_template('LizzyLohmann.html', comments=comments)

@app.route('/brenna_gogel')
def brenna_gogel():
    comments = page_comments.get('brenna_gogel', [])
    return render_template('BrennaGogel.html', comments=comments)

@app.route('/chase_dittmer')
def chase_dittmer():
    comments = page_comments.get('chase_dittmer', [])
    return render_template('ChaseDittmer.html', comments=comments)


@app.route('/register')
def register():
    # Your code here
    return render_template('register.html')

@app.route('/login')
def login():
    # Your code here
    return render_template('login.html')

@app.route('/add_comment/<page>', methods=['POST'])
def add_comment(page):
    new_comment = request.form['comment']

    # Get the list of comments for the specific page or create an empty list if not exists
    comments = page_comments.get(page, [])
    comments.append(new_comment)
    page_comments[page] = comments

    # Redirect to the specific page with the 'page' parameter
    return redirect(url_for(page, page=page))


@app.route('/add', methods=['POST'])
def add():
    # Add data to MongoDB
    new_data = {
        'username': request.form['username'],
        'password': request.form['password']
    }
    collection.insert_one(new_data)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
