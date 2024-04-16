from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class PredictForm(FlaskForm):
    url = URLField('Youtube URL', validators=[DataRequired()])
    submit = SubmitField('Predict')
