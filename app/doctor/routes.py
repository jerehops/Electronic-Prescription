from app.doctor import bp
from app import db
from flask import render_template
from flask_login import login_required


@bp('/create-rescription', methods=['GET', 'POST'])
def create_prescriptions():
    return render_template('doctor/create_prescriptions.html')
