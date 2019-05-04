from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BookCategory, Books, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r')
                       .read())['web']['client_id']

engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User helper function
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
                   json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps
                                 ("Token's user ID doesn't match given user"
                                  "ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected'
                                  '.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    print('Access Token is &&&&&&&&&&&&&&&&&')
    print(credentials.access_token)
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # create or fetch user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    return login_session['username']


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps
                                 ('Current user not'
                                  'connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': access_token},
                           headers={'content-type': 'application/x-www-form-'
                                    'urlencoded'})
    result = getattr(revoke, 'status_code')
    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        print("Status code is 200")
        del login_session['access_token']
        del login_session['gplus_id']
    response = make_response(json.dumps('Disconnected.'), 200)
    print(response)
    redirect('/login')
    return response


# fb connect
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secret.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secret.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client'
           '_secret=%s&fb_exchange_token'
           '=%s' % (app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.2/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first
        index which gives us the key :value for the server access token then
        we split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly in
        the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v3.2/me?access_token'
           '=%s&fields=name,id,email' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = ('https://graph.facebook.com/v3.2/me/picture?access_token'
           '=%s&redirect=0&height=200&width=200' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # create or fetch user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    return login_session['username']


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token'
           '=%s' % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['access_token']
    del login_session['facebook_id']
    return result


@app.route('/disconnect')
def disconnect():
    if login_session['provider'] == 'google':
        gdisconnect()
    else:
        fbdisconnect()
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['provider']


@app.route('/')
@app.route('/catalog')
def getBookCatalog():
    categories = session.query(BookCategory).all()
    top10 = (session.query(Books)
             .order_by(Books.updated_at.desc())
             .limit(10).all())
    if 'username' not in login_session:
        return render_template('publicCatalog.html', categories=categories,
                               books=top10)
    else:
        return render_template('catalog.html', categories=categories,
                               books=top10, login_session=login_session)


@app.route('/catalog/<int:category_id>/')
def getAllBooksForCategory(category_id):
    categories = session.query(BookCategory).all()
    category = session.query(BookCategory).filter_by(id=category_id).one()
    books = session.query(Books).filter_by(category_id=category_id).all()
    return render_template('catalog.html', books=books, category=category,
                           categories=categories,
                           login_session=login_session)


@app.route('/catalog/create', methods=['GET', 'POST'])
def createCategory():
    if request.method == 'POST':
        newCategory = BookCategory(name=request.form['category_name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('getBookCatalog', login_session=login_session))
    else:
        return render_template('add_category.html',
                               login_session=login_session)


@app.route('/catalog/addItem', methods=['GET', 'POST'])
def addItem():
    categories = session.query(BookCategory).all()
    if request.method == 'POST':
        categoryName = request.form['categoryName']
        categoryId = (session.query(BookCategory)
                      .filter_by(name=categoryName)
                      .one().id)
        newBook = Books(name=request.form['name'],
                        description=request.form['description'],
                        author=request.form['author'],
                        price=request.form['price'],
                        category_id=categoryId,
                        user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('getBookCatalog', login_session=login_session))
    else:
        return render_template('add_book.html', categories=categories,
                               login_session=login_session)


@app.route('/catalog/<int:category_id>/book/<int:book_id>')
def bookDetails(category_id, book_id):
    category = session.query(BookCategory).filter_by(id=category_id).one()
    book = session.query(Books).filter_by(id=book_id).one()
    if ('user_id' not in login_session or
       book.user_id != login_session['user_id']):
        return render_template('publicBook_details.html', category=category,
                               book=book, login_session=login_session)
    else:
        return render_template('book_details.html', category=category,
                               book=book, login_session=login_session)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def editBook(book_id):
    categories = categories = session.query(BookCategory).all()
    book = session.query(Books).filter_by(id=book_id).one()
    category_name = (session.query(BookCategory)
                     .filter_by(id=book.category_id)
                     .one().name)
    if request.method == 'POST':
        categoryName = request.form['categoryName']
        category = (session.query(BookCategory)
                    .filter_by(name=categoryName)
                    .one())
        book.name = request.form['name']
        book.description = request.form['description']
        book.author = request.form['author']
        book.price = request.form['price']
        book.category_id = category.id
        return redirect(url_for('bookDetails', category_id=category.id,
                                book_id=book.id, login_session=login_session))
    else:
        return render_template('edit_book.html', book=book,
                               categories=categories,
                               category_name=category_name,
                               login_session=login_session)


@app.route('/catalog/<int:category_id>/book/<int:book_id>/delete/',
           methods=['POST', 'GET'])
def deleteBook(book_id, category_id):
    category = session.query(BookCategory).filter_by(id=category_id).one()
    book = session.query(Books).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        return redirect(url_for('getBookCatalog', login_session=login_session))
    else:
        return render_template('delete_book.html', book=book,
                               category=category, login_session=login_session)


@app.route('/catalog.json')
def getBookDetails():
    books = session.query(Books).all()
    return jsonify(books=[i.serialize for i in books])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
