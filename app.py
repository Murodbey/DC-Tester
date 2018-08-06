from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, TextField
from flask import Flask, render_template, redirect, url_for, request
from wtforms.validators import InputRequired, Email, Length
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask_wtf import FlaskForm, RecaptchaField
from flask_sqlalchemy  import SQLAlchemy
from flask_bootstrap import Bootstrap
import commands
import os

app = Flask(__name__)


app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase/database.db'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeBCGAUAAAAAHbgwWpZJSPsTZg4NB6xG50EfJUA'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeBCGAUAAAAAA9-6zznkZbVmFJMy7gw1uQq8PEl'
app.config['TESTING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15))
    lastname = db.Column(db.String(15))
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(10))
    password = db.Column(db.String(80))

class Servers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.String(15))
    name = db.Column(db.String(11))
    password = db.Column(db.String(80))
    student = db.Column(db.String(30))
    status = db.Column(db.String(10))


class myModelView(ModelView):
    def is_accessible(self):
        if current_user.role == "Admin":
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return "<h2> Sorry you dont have permission for this page <h2>"


class MyAdminIndex(AdminIndexView):
    def is_accessible(self):
        if current_user.role == "Admin":
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return "<h2> Sorry you dont have permission for this page<h2>"




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    recaptcha = RecaptchaField()

class RegisterForm(FlaskForm):
    firstname = StringField('Fistname', validators=[InputRequired(), Length(max=15)])
    lastname = StringField('Lastname', validators=[InputRequired(), Length(max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()

class servers(FlaskForm):
    ipaddr = StringField('ipaddr', validators=[InputRequired(), Length(min=7, max=24)])


@app.route('/raiting', methods=['GET', 'POST'])
@login_required
def raiting():
    return render_template('raiting.html')

@app.route('/sshcopy', methods=['GET', 'POST'])
@login_required
def sshcopy():
    return render_template('sshcopy.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    fullName = current_user.firstname + " " + current_user.lastname
    servers = Servers.query.filter_by(student=fullName)


    if 'repoip' in request.form:
        ipaddr = request.form['repoip']
        result = commands.getstatusoutput('ls')
        with open('ips.txt', 'w') as the_file:
            the_file.write(ipaddr)
        with open('scripts/info.txt', 'w') as the_file:
            the_file.write(ipaddr)
        result = commands.getoutput('sh scripts/repository/yum_test.sh')
        name = "Repository"
        if result == "DONE":
            server = Servers.query.filter_by(name="Repository").first()
            server.status = "DONE"
            server.ipaddr = ipaddr
            db.session.commit()
        else:
            server = Servers.query.filter_by(name="Repository").first()
            server.status = "NONE"
            db.session.commit()

        return render_template('check.html', result=result, ipaddr=ipaddr, name=name)

    elif 'dnsip' in request.form:
        ipaddr = request.form['dnsip']
        dnsname = request.form['dnsname']
        with open('ips.txt', 'w') as the_file:
            the_file.write("[dns]" + '\n' + ipaddr)
        with open('scripts/info.txt', 'w') as the_file:
            the_file.write(ipaddr + " " + dnsname)
        result = commands.getoutput('sh scripts/dns-server/dnscheck.sh')
        if result == "DONE":
            server = Servers.query.filter_by(name="DNS-Server").first()
            server.status = "DONE"
            server.ipaddr = ipaddr
            db.session.commit()
        else:
            server = Servers.query.filter_by(name="DNS-Server").first()
            server.status = "NONE"
            db.session.commit()
        name = "DNS Server"
        return render_template('check.html', result=result, ipaddr=ipaddr, name=name)

    elif 'webip' in request.form:
         ipaddr = request.form['webip']
         with open('scripts/info.txt', 'w') as the_file:
             the_file.write(ipaddr)
         result = commands.getoutput('sh scripts/mail-server/mail-server.sh')
         name = "Webserver"
         if result == "DONE":
             server = Servers.query.filter_by(name="Webserver").first()
             server.status = "DONE"
             server.ipaddr = ipaddr
             db.session.commit()
         else:
             server = Servers.query.filter_by(name="Webserver").first()
             server.status = "NONE"
             db.session.commit()
         return render_template('check.html', result=result, ipaddr=ipaddr, name=name)

    elif 'webip' in request.form:
         ipaddr = request.form['webip']
         with open('scripts/info.txt', 'w') as the_file:
             the_file.write(ipaddr)
         result = commands.getoutput('sh scripts/mail-server/mail-server.sh')
         name = "Webserver"
         if result == "DONE":
             server = Servers.query.filter_by(name="Webserver").first()
             server.status = "DONE"
             server.ipaddr = ipaddr
             db.session.commit()
         else:
             server = Servers.query.filter_by(name="Webserver").first()
             server.status = "NONE"
             db.session.commit()
         return render_template('check.html', result=result, ipaddr=ipaddr, name=name)

    elif 'ansible' in request.form:
         ipaddr = request.form['ansible']
         with open('scripts/info.txt', 'w') as the_file:
             the_file.write(ipaddr)
         result = commands.getoutput('sh scripts/mail-server/mail-server.sh')
         name = "Ansible"
         if result == "DONE":
             server = Servers.query.filter_by(name="Ansible").first()
             server.status = "DONE"
             server.ipaddr = ipaddr
             db.session.commit()
         else:
             server = Servers.query.filter_by(name="Ansible").first()
             server.status = "NONE"
             db.session.commit()
         return render_template('check.html', result=result, ipaddr=ipaddr, name=name)

    elif 'ipnfs' in request.form:
         ipaddr = request.form['ipnfs']
         with open('scripts/info.txt', 'w') as the_file:
             the_file.write(ipaddr)
         result = commands.getoutput('sh scripts/mail-server/mail-server.sh')
         name = "NFS-Server"
         if result == "DONE":
             server = Servers.query.filter_by(name="NFS-Server").first()
             server.status = "DONE"
             server.ipaddr = ipaddr
             db.session.commit()
         else:
             server = Servers.query.filter_by(name="NFS-Server").first()
             server.status = "NONE"
             db.session.commit()
         return render_template('check.html', result=result, ipaddr=ipaddr, name=name)

    return render_template('dashboard.html', name=current_user.username, servers=servers)



@app.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    return render_template('check.html' )

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        fullName = form.firstname.data + " " + form.lastname.data
        objects = [  Servers(name="Repository", status="NONE", student=fullName),  Servers(name="DNS-Server", status="NONE", student=fullName),  Servers(name="MYSQL", status="NONE", student=fullName), Servers(name="Mail-Server", status="NONE", student=fullName), Servers(name="Nagios", status="NONE", student=fullName), Servers(name="Webserver", status="NONE", student=fullName),   Servers(name="Ansible", status="NONE", student=fullName),  Servers(name="NFS-Server", status="NONE", student=fullName), User(lastname=form.lastname.data, firstname=form.firstname.data, username=form.username.data, email=form.email.data, password=hashed_password, role="student")]
        db.session.add_all(objects)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


admin = Admin(app, index_view=MyAdminIndex())
admin.add_view(myModelView(User, db.session))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True )
