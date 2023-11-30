from datetime import timedelta
import certifi
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_login import LoginManager, UserMixin, login_required
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__, static_folder='templates/static')
app.secret_key = 'test1'
app.permanent_session_lifetime = timedelta(minutes=1)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Connect to MongoDB
uri = "mongodb+srv://justin:test@lab3.swakhcz.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsCAFile=certifi.where())

db = client.get_database('Lab3')  # Specify the database name
collection = db['users']  # Use 'users' as the collection name
comments_collection = db['comments']


# Initialize a dictionary to store comments for each page
page_comments = {
    'justin_schumacher': [],
    'lizzy_lohmann': [],
    'brenna_gogel': [],
    'chase_dittmer': [],
}

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    # Retrieve user from the database
    user_data = collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        user = User()
        user.id = str(user_data['_id'])
        return user
    return None

@app.route('/')
def index():
    # Retrieve data from MongoDB
    data = collection.find()
    return render_template('index.html', data=data)


@app.route('/justin_schumacher')
def justin_schumacher():
    comments_document = comments_collection.find_one({'page': 'justin_schumacher'})

    if comments_document:
        page_comments['justin_schumacher'] = comments_document.get('comments', [])
    else:
        # Handle the case where no comments document is found
        page_comments['justin_schumacher'] = []
    if 'username' in session:
        return render_template('JustinSchumacher.html', comments=page_comments.get('justin_schumacher', []))
    else:
        return render_template('index.html', error="Please log in before accessing profile pages.")


@app.route('/lizzy_lohmann')
def lizzy_lohmann():
    comments_document = comments_collection.find_one({'page': 'lizzy_lohmann'})

    if comments_document:
        page_comments['lizzy_lohmann'] = comments_document.get('comments', [])
    else:
        # Handle the case where no comments document is found
        page_comments['lizzy_lohmann'] = []
    if 'username' in session:
        return render_template('LizzyLohmann.html', comments=page_comments.get('lizzy_lohmann', []))
    else:
        return render_template('index.html', error="Please log in before accessing profile pages.")

@app.route('/brenna_gogel')
def brenna_gogel():
    comments_document = comments_collection.find_one({'page': 'brenna_gogel'})

    if comments_document:
        page_comments['brenna_gogel'] = comments_document.get('comments', [])
    else:
        # Handle the case where no comments document is found
        page_comments['brenna_gogel'] = []
    if 'username' in session:
        return render_template('BrennaGogel.html', comments=page_comments.get('brenna_gogel', []))
    else:
        return render_template('index.html', error="Please log in before accessing profile pages.")

@app.route('/chase_dittmer')
def chase_dittmer():
    comments_document = comments_collection.find_one({'page': 'chase_dittmer'})

    if comments_document:
        page_comments['chase_dittmer'] = comments_document.get('comments', [])
    else:
        # Handle the case where no comments document is found
        page_comments['chase_dittmer'] = []
    if 'username' in session:
        return render_template('ChaseDittmer.html', comments=page_comments.get('chase_dittmer', []))
    else:
        return render_template('index.html', error="Please log in before accessing profile pages.")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        existing_user = collection.find_one({'username': username})

        if existing_user:
            # Username already exists, you can provide an error message or redirect to a registration error page
            return render_template('register.html', error='Username already exists. Please choose another username.')

        # If the username is not in the database, add the new user
        new_data = {
            'username': username,
            'password': password,
        }
        try:
            collection.insert_one(new_data)
            print("User inserted successfully")
        except Exception as e:
            print(f"Error inserting user data: {e}")

        # Redirect to the index or login page after successful registration
        return redirect(url_for('index'))

    # If the request method is GET, render the registration form
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username, 'password': password})

        if user:
            session.permanent = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='User does not exist.')

    return render_template('login.html')

@app.route('/add_comment/<page>', methods=['POST'])
def add_comment(page):
    new_comment = request.form['comment']

    # Get the list of comments for the specific page or create an empty list if not exists
    comments = page_comments.get(page, [])
    comments.append(new_comment)
    page_comments[page] = comments

    # Save the comments to MongoDB
    comments_collection.update_one(
        {'page': page},
        {'$set': {'comments': comments}},
        upsert=True
    )

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
