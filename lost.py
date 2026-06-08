from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from form import RegistrationForm, LoginForm, LostItemForm, FoundItemForm, SearchForm
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(
        db.String(50),
        nullable=False
    )

   
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    lost_items = db.relationship(
        'LostItem',
        backref='owner',
        lazy=True
    )

    found_items = db.relationship(
        'FoundItem',
        backref='owner',
        lazy=True,
        foreign_keys='FoundItem.user_id'
    )

    claimed_items = db.relationship(
        'FoundItem',
        backref='claimer',
        lazy=True,
        foreign_keys='FoundItem.claimed_by'
    )   

class LostItem(db.Model):

    __tablename__ = "lost_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )
    image_path = db.Column(
            db.String(255)
        )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    date_lost = db.Column(
        db.Date,
        nullable=False
    )

    contact_phone = db.Column(
        db.String(20),
        nullable=False
    )

    
    status = db.Column(
        db.String(20),
        default="Lost"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
         nullable=False
    )

class FoundItem(db.Model):

    __tablename__ = "found_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    date_found = db.Column(
        db.Date,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    image_path = db.Column(
        db.String(255)
    )

    status = db.Column(
        db.String(20),
        default="Found"
    )

    claimed_by= db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    is_claimed=db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

class ClaimRequest(db.Model):

    __tablename__="claim_requests"


    id=db.Column(
        db.Integer,
        primary_key=True
    )


    found_item_id=db.Column(
        db.Integer,
        db.ForeignKey('found_items.id'),
        nullable=False
    )


    requester_id=db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )


    status=db.Column(
        db.String(20),
        default="Pending"
    )


    message=db.Column(
        db.Text
    )


    item=db.relationship(
        "FoundItem"
    )


    requester=db.relationship(
        "User"
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
@login_required
def about():

    return render_template(
        "about.html"
    )

@app.route("/lost", methods=["GET", "POST"])
@login_required
def lost():
    form = LostItemForm()
    if form.validate_on_submit():
        # Here you would typically save the lost item to the database
        if request.method == "POST":
            item_name = form.item_name.data
            category = form.category.data
            description = form.description.data
            item_image = form.item_image.data
            filename = secure_filename(item_image.filename)
            item_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            location = form.location.data
            date_lost = form.date_lost.data
            phone = form.phone.data

            new_lost_item = LostItem(
                item_name=item_name,
                category=category,
                description=description,
                image_path=filename,
                location=location,
                date_lost=date_lost,
                contact_phone=phone,
                user_id=current_user.id
            )
            db.session.add(new_lost_item)
            db.session.commit()



        flash('Lost item reported successfully!', 'success')
        return redirect(url_for('home'))
    return render_template("lost.html", form=form)

@app.route("/found", methods=["GET", "POST"])
@login_required
def found():
    form = FoundItemForm()
    if form.validate_on_submit():
        # Here you would typically save the found item to the database
        if request.method == "POST":
            item_name = form.item_name.data
            category = form.category.data
            description = form.description.data
            item_image = form.item_image.data
            filename = secure_filename(item_image.filename)
            item_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            location = form.location.data
            date_found = form.date_found.data
            phone = form.phone.data

            new_found_item = FoundItem(
                item_name=item_name,
                category=category,
                description=description,
                image_path=filename,
                location=location,
                date_found=date_found,
                phone=phone,
                user_id=current_user.id
            )
            db.session.add(new_found_item)
            db.session.commit()

        flash('Found item reported successfully!', 'success')
        return redirect(url_for('home'))
    return render_template("found.html", form=form)

@app.route("/list", methods=["GET", "POST"])
@login_required
def list():

    form = SearchForm()


    query = FoundItem.query.filter_by(
        is_claimed=False
    )


    category = request.args.get("category")

    sort = request.args.get("sort")


    search = request.args.get("search")



    if category:

        query = query.filter_by(
            category=category
        )



    if search:

        query = query.filter(
            FoundItem.item_name.contains(search)
        )



    if sort == "latest":

        query = query.order_by(
            FoundItem.date_found.desc()
        )


    elif sort == "oldest":

        query = query.order_by(
            FoundItem.date_found.asc()
        )


    elif sort == "name":

        query = query.order_by(
            FoundItem.item_name.asc()
        )


    found_items = query.all()



    return render_template(
        "list.html",
        form=form,
        found_items=found_items
    )

@app.route("/claim/<int:id>", methods=["POST"])
@login_required
def claim(id):

    item=FoundItem.query.get_or_404(id)


    existing=ClaimRequest.query.filter_by(
        found_item_id=id,
        requester_id=current_user.id
    ).first()


    if existing:

        flash(
        "Request already sent",
        "warning"
        )

        return redirect(url_for("list"))


    request=ClaimRequest(

        found_item_id=id,
        requester_id=current_user.id,
        message="I believe this item belongs to me"
    )


    db.session.add(request)
    db.session.commit()


    flash(
    "Claim request sent",
    "success"
    )


    return redirect(url_for("list"))


@app.route("/requests")
@login_required
def requests():

    req=ClaimRequest.query.join(
        FoundItem
    ).filter(
        FoundItem.user_id==current_user.id,
        ClaimRequest.status=="Pending"
    ).all()


    return render_template(
        "requests.html",
        requests=req
    )

@app.route("/accept_claim/<int:id>",methods=["POST"])
@login_required
def accept_claim(id):

    req=ClaimRequest.query.get_or_404(id)


    req.status="Accepted"


    req.item.claimed=True

    req.item.status="Claimed"


    db.session.commit()


    flash(
    "Item claimed successfully",
    "success"
    )


    return redirect(url_for("requests"))

@app.route("/reject_claim/<int:id>",methods=["POST"])
@login_required
def reject_claim(id):

    req=ClaimRequest.query.get_or_404(id)


    req.status="Rejected"


    db.session.commit()


    return redirect(
        url_for("requests")
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here you would typically save the user to the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if request.method == "POST":
            fullname = form.fullname.data
            username = form.username.data
            email = form.email.data
            phone = form.phone.data
            password = hashed_password

            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('Username or email already exists. Please choose a different one.', 'danger')
                return redirect(url_for('register'))

            new_user = User(fullname=fullname, username=username, email=email, phone=phone, password=password)
            db.session.add(new_user)
            db.session.commit()






        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Here you would typically validate the user credentials
        user = User.query.filter_by(username=form.username.data).first()
        if  user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            flash('Logged in successfully!', 'success')
            return redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
    "You have been logged out",
    "success"
    )

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
with app.app_context():
        db.create_all()