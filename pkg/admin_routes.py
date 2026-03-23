from flask import render_template,request,redirect,flash,make_response,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from pkg import app
from pkg.models import Admin,Player,Scout,db
from pkg.forms import Login




@app.route('/admin/login/',methods=['GET','POST'])
def admin_login():
    login = Login()
    if request.method == 'GET':
        return render_template('admin/admin_login.html',login=login)
    else:
        if login.validate_on_submit():
            email = login.email.data
            password = login.password.data
            admin = Admin.query.filter(Admin.admin_email==email).first()
            if admin:
                stored_password = admin.admin_password_hash
                check = check_password_hash(stored_password,password)
                if check:
                    session['adminonline'] = admin.admin_username
                    session['adminid'] = admin.admin_id
                    session['usertype'] = 'admin'
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash("Invalid credentials",category='danger')
                    return redirect(url_for('admin_login'))
            else:
                flash("Invalid credentials",category='danger')
                return redirect(url_for('admin_login'))
        else:
            return render_template('admin/login.html',login=login)
        


@app.route('/admin/logout/')
def admin_logout():
    if session.get('adminonline') and session.get('adminid'):
        session.pop('adminonline',None)
        session.pop('adminid',None)
        session.clear()
    return redirect(url_for('admin_login'))




@app.route("/admin/",methods=['POST','GET'])
def admin_home():
    if session.get('adminonline') and session.get('adminid'):
        return redirect(url_for('admin_dashboard'))
    else:
        flash("you must be logged in as an admin",category='danger')
        return redirect(url_for('admin_login'))




@app.route('/admin/dashboard/')
def admin_dashboard():
    players = Player.query.all()
    scouts = Scout.query.all()
    if session.get('adminonline') and session.get('adminid'):
        return render_template('admin/admin_dashboard.html',players=players,scouts=scouts,total_players=len(players),total_scouts=len(scouts),total_users=len(players) + len(scouts))
    else:
        flash("you must be logged in as an admin",category='danger')
        return redirect(url_for('admin_login'))



























# @app.route('/insert/admin/')
# def insert_admin():
#     admin = Admin(admin_username="Emerikos",admin_email="Emerikosadmin@gmail.com",admin_password_hash=generate_password_hash("1234"))
#     db.session.add(admin)
#     db.session.commit()
#     return "Admin added"