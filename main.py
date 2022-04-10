import wtforms.validators
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import URLField, TimeField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

CAFE_SYMBOL = "☕"
WIFI_SYMBOL = "💪"
SOCKET_SYMBOL = "🔌"

coffee_ratings = []
wifi_ratings = []
socket_ratings = []

for i in range(1, 6):
    coffee_ratings.append(CAFE_SYMBOL * i)
    wifi_ratings.append(WIFI_SYMBOL * i)
    socket_ratings.append(SOCKET_SYMBOL * i)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = URLField('Cafe Location on Google Maps (URL)',
                   validators=[DataRequired(), wtforms.validators.URL(require_tld=True)])
    opening = TimeField('Opening Time e.g. 8:00AM', validators=[DataRequired()])
    closing = TimeField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Rating', choices=coffee_ratings)
    wifi = SelectField(u'Wifi Strength Rating', choices=wifi_ratings)
    socket = SelectField(u'Power Socket Availability', choices=socket_ratings)
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = f"\n" \
                   f"{form.cafe.data}," \
                   f"{form.url.data}," \
                   f"{form.opening.data}," \
                   f"{form.closing.data}," \
                   f"{form.coffee_rating.data}," \
                   f"{form.wifi.data}," \
                   f"{form.socket.data}"
        with open('cafe-data.csv', "a", encoding="utf8", newline="") as csv_file:
            csv_file.write(new_cafe)
            csv_file.close()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding="utf8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', len=len(list_of_rows), cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
