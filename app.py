from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserInfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ParentUser(db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.String(4))
    child = db.relationship('ChildUser', backref='parent', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, first_name, last_name, street, city, state, zip_code):
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip_code


class ChildUser(db.Model):
    __tablename__ = 'child'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    parent_id = db.Column(db.String, db.ForeignKey('parent.id'), nullable=False)
    parent_first_name = db.Column(db.String(100))
    parent_last_name = db.Column(db.String(100))

    def __init__(self, first_name, last_name, parent_id, parent_first_name, parent_last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.parent_id = parent_id
        self.parent_first_name = parent_first_name
        self.parent_last_name = parent_last_name


@app.route('/')
def index():
    all_parent_user = ParentUser.query.all()
    all_child_user = ChildUser.query.all()

    return render_template("index.html", parent_user=all_parent_user, child_user=all_child_user)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']

        parent_user = ParentUser(first_name, last_name, street, city, state, zip_code)
        db.session.add(parent_user)
        db.session.commit()

        flash("User inserted successfully")

        return redirect(url_for('index'))


@app.route('/insert_child', methods=['POST'])
def insert_child():
    if request.method == 'POST':
        first_name_child = request.form['firstnamechild']
        last_name_child = request.form['lastnamechild']
        parent_user = ParentUser.query.get(request.form.get("parentid"))
        if parent_user is None:
            flash("No parent user exists for this id")
            return redirect(url_for('index'))

        parent_id = parent_user.id
        parent_first_name = parent_user.first_name
        parent_last_name = parent_user.last_name

        child_user = ChildUser(first_name_child, last_name_child, parent_id, parent_first_name, parent_last_name)
        db.session.add(child_user)
        db.session.commit()

        flash("User inserted successfully")
        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        parent_user = ParentUser.query.get(request.form.get("id"))
        parent_user.first_name = request.form['firstname']
        parent_user.last_name = request.form['lastname']
        parent_user.street = request.form['street']
        parent_user.city = request.form['city']
        parent_user.state = request.form['state']
        parent_user.zip_code = request.form['zip']

        db.session.commit()
        flash("User updated successfully")

        return redirect(url_for('index'))


@app.route('/update_child', methods=['GET', 'POST'])
def update_child():
    if request.method == 'POST':
        child_user = ChildUser.query.get(request.form.get("id"))
        child_user.first_name = request.form['firstnamechild']
        child_user.last_name = request.form['lastnamechild']
        parent_user = ParentUser.query.get(request.form.get("parentid"))

        if parent_user is None:
            flash("No parent user exists for this id")
            return redirect(url_for('index'))

        child_user.parent_id = parent_user.id
        child_user.parent_first_name = parent_user.first_name
        child_user.parent_last_name = parent_user.last_name

        db.session.commit()
        flash("User updated successfully")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(parent_id):
    parent_user = ParentUser.query.get(parent_id)
    db.session.delete(parent_user)
    db.session.commit()
    flash("User Deleted Successfully")

    return redirect(url_for('index'))


@app.route('/delete_child/<id>/', methods=['GET', 'POST'])
def delete_child(child_id):
    child_user = ChildUser.query.get(child_id)
    db.session.delete(child_user)
    db.session.commit()
    flash("User Deleted Successfully")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
