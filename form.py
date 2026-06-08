from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField,EmailField,PasswordField,SelectField,DateTimeLocalField,FileField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class RegistrationForm(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Full Name"})
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    email = EmailField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "Phone Number"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class LostItemForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired()], render_kw={"placeholder": "Item Name"})
    category = SelectField("Category", choices=[
        ("", "-- Select Category --"),
        ("Electronics", "Electronics"),
        ("Clothes", "Clothes"),
        ("Books", "Books"),
        ("Documents", "Documents"),
        ("Accessories", "Accessories"),
        ("Bags", "Bags"),
        ("Jewellery", "Jewellery"),
        ("Mobile Phones", "Mobile Phones"),
        ("Laptop", "Laptop"),
        ("Keys", "Keys"),
        ("Wallet", "Wallet"),
        ("ID Cards", "ID Cards"),
        ("Sports Items", "Sports Items"),
        ("Others", "Others")
    ], validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()], render_kw={"placeholder": "Description"})
    item_image = FileField("Item Image", validators=[DataRequired()], render_kw={"placeholder": "Image URL"})
    location = StringField("Location", validators=[DataRequired()], render_kw={"placeholder": "Location"})
    date_lost = DateTimeLocalField("Date Lost", validators=[DataRequired()], render_kw={"placeholder": "Date Lost"})
    phone = StringField("Contact Phone", validators=[DataRequired()], render_kw={"placeholder": "Contact Phone"})
    submit = SubmitField("Report Lost Item")

class FoundItemForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired()], render_kw={"placeholder": "Item Name"})
    category = SelectField("Category", choices=[
        ("", "-- Select Category --"),
        ("Electronics", "Electronics"),
        ("Clothes", "Clothes"),
        ("Books", "Books"),
        ("Documents", "Documents"),
        ("Accessories", "Accessories"),
        ("Bags", "Bags"),
        ("Jewellery", "Jewellery"),
        ("Mobile Phones", "Mobile Phones"),
        ("Laptop", "Laptop"),
        ("Keys", "Keys"),
        ("Wallet", "Wallet"),
        ("ID Cards", "ID Cards"),
        ("Sports Items", "Sports Items"),
        ("Others", "Others")
    ], validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()], render_kw={"placeholder": "Description"})
    item_image = FileField("Item Image", validators=[DataRequired()], render_kw={"placeholder": "Image URL"})
    location = StringField("Location", validators=[DataRequired()], render_kw={"placeholder": "Location"})
    date_found = DateTimeLocalField("Date Found", validators=[DataRequired()], render_kw={"placeholder": "Date Found"})
    phone = StringField("Contact Phone", validators=[DataRequired()], render_kw={"placeholder": "Contact Phone"})
    submit = SubmitField("Report Found Item")

class SearchForm(FlaskForm):

    keyword = StringField(
        "Search Item",
        render_kw={
        "placeholder":"Search item name"
        }
    )


    category = SelectField(
        "Category",
        choices=[
         ("", "-- Select Category --"),
        ("Electronics", "Electronics"),
        ("Clothes", "Clothes"),
        ("Books", "Books"),
        ("Documents", "Documents"),
        ("Accessories", "Accessories"),
        ("Bags", "Bags"),
        ("Jewellery", "Jewellery"),
        ("Mobile Phones", "Mobile Phones"),
        ("Laptop", "Laptop"),
        ("Keys", "Keys"),
        ("Wallet", "Wallet"),
        ("ID Cards", "ID Cards"),
        ("Sports Items", "Sports Items"),
        ("Others", "Others")
        ]
    )


    submit = SubmitField("Search")