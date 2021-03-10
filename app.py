from flask import Flask, _app_ctx_stack, jsonify, url_for, render_template, session, redirect
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import scoped_session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Optional


from globals import *
from model import *
from database import SessionLocal, engine


app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
bootstrap = Bootstrap(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
db = SessionLocal()


#################
###           ###
###   Forms   ###
###           ###
#################

class CometForm(FlaskForm):
    name = StringField('Name - optional',validators=[Optional()])
    email = StringField('Email - needed to send you your password', validators=[DataRequired(), Email()])
    optin = BooleanField('Newsleter opt in - sent approximately once a month to update you on the project')
    submit = SubmitField('Gimme Comet!')

class CodeForm(FlaskForm):
    hidden = StringField(None)
    submit = SubmitField("Go!")
    
 
    
##################
###            ###
###   Routes   ###
###            ###
##################

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    email = None
    optin = False
    form = CometForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        optin = form.optin.data
        
        # create new user as needed
        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            user = Users(name, email, optin)            
            db.add(user)
            db.commit()
        
        # assign comet to user
        comet = db.query(Comet).filter(Comet.status == CometStatus.READY).first()
        if not comet:
            os._exit()   # TODO graceful error handling
        comet.assigned = user.id
        comet.assigned_ts = datetime.now()
        comet.status = CometStatus.ASSIGNED
        db.commit()
        
        # build redirect link
        comet_link = 'http://' + HOST + str(comet.port)
        session["link"] = comet_link
        session["code"] = comet.code
        return redirect(url_for('code'))
    
    return render_template('index.html', form=form)


@app.route('/code', methods=['GET', 'POST'])
def code():
    form = CodeForm()
    if form.is_submitted():
        return redirect(session.get("link"))
    return render_template('code.html', code=session.get("code"), link=session.get("link"))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
