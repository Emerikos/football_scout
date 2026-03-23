import secrets,os
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from flask import render_template,request,redirect,flash,make_response,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from pkg import app
from pkg.forms import RegisterPlayer,RegisterScout,Login,safe_enum,Profileform,PhotoForm,ScoutProfileform
from pkg.models import db,Player,PlayerPosition,Position,Scout,Video,Country


@app.errorhandler(404)
def mypagenotfound(error):
    return render_template('user/404.html',error=error),404


@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache','no-store','must-revalidate'
    return response  



@app.route('/')
def home():
    play = Player.query.order_by(func.random()).limit(5).all()
    return render_template('user/index.html',play=play)
    

@app.route('/about/')
def about():
    return render_template('user/about.html')

@app.route('/register-player/',methods=['GET','POST'])
def player_register():
    form = RegisterPlayer() 
    positions = Position.query.all()
    form.primary_position.choices = [(position.position_id,position.position_name) for position in positions]
    form.secondary_positions.choices = [(position.position_id, position.position_name) for position in positions]
    if request.method == 'GET':
        return render_template('user/register_player.html',form=form)
    else:
        if form.validate_on_submit():
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            hashed_password = generate_password_hash(password)
            dob = request.form.get('dob')
            countryName = request.form.get('country')
            primary_position = request.form.get('primary_position')
            height = request.form.get('height')
            phone_number = request.form.get('phone_number')
            # preferred_foot = request.form.get('preferred_foot')
            # normalize_foot = safe_enum(preferred_foot, ["left", "right", "both"])

            country = Country.query.filter(Country.country_name==countryName).first()
            new_player = Player(
                player_firstname=firstname,player_lastname=lastname,player_password_hash=hashed_password,
                player_email=email,player_date_of_birth=dob,player_height=height,player_phone=phone_number,country_id=country.country_id,
                primary_position_id=primary_position
                # player_pref_foot=normalize_foot
            )
            if Player.is_email_used(email):
                flash("You have registered before, Please login " + email,category='danger')
                return redirect(url_for('player_login'))
            else:
                db.session.add(new_player)
                db.session.commit()
            for position_id in form.secondary_positions.data:
                if position_id == form.primary_position.data:
                    continue
                secondary = PlayerPosition(
                    player_id = new_player.player_id,
                    position_id = position_id
                )
                db.session.add(secondary)
            db.session.commit()
            flash("Player registration successful,please login",category='success')
            return redirect(url_for('player_login'))
        else:
            return render_template('user/register_player.html',form=form)


@app.route('/register-scout/',methods=["GET",'POST'])
def scout_register():
    f = RegisterScout()
    if request.method == 'GET':
        return render_template('user/register_scout.html',f=f)
    else:
        if f.validate_on_submit():
            firstname = request.form.get('firstname_scout')
            lastname = request.form.get('lastname_scout')
            email = request.form.get('email_scout')
            password = request.form.get('password_scout')
            hashed_password = generate_password_hash(password)
            new_scout = Scout(scout_firstname=firstname,scout_lastname=lastname,email=email,scout_password_hash=hashed_password)
            if Scout.is_email_used(email):
                flash("You have registered before, Please login " + email,category='danger')
                return redirect(url_for('scout_login'))
            else:
                db.session.add(new_scout)
                db.session.commit()
                flash("Scout registration successful",category='success')
                return redirect(url_for('scout_login'))
        else:
            return render_template('user/register_scout.html',f=f)
    


@app.route('/login/player/',methods=['GET','POST'])
def player_login():
    log = Login()
    if request.method == 'GET':
        return render_template('user/login.html',log=log)
    else:
        if log.validate_on_submit():
            email = log.email.data
            password = log.password.data
            userdeets = Player.query.filter(Player.player_email==email).first()
            if userdeets:
                stored_password = userdeets.player_password_hash
                check = check_password_hash(stored_password,password)
                if check == True:
                    session["useronline"] = userdeets.player_firstname
                    session["userid"] = userdeets.player_id
                    session["usertype"] = "player"
                    return redirect(url_for('profile'))
                else:
                    flash("Invalid credentials",category="danger")
                    return redirect(url_for('player_login'))
            else:
                flash("Invalid credentials",category="danger")
                return redirect(url_for('player_login'))
        else:
            return render_template("user/login.html",log=log)
        





@app.route('/login/scout/',methods=['GET','POST'])
def scout_login():
    log = Login()
    if request.method == 'GET':
        return render_template('user/login.html',log=log)
    else:
        if log.validate_on_submit():
            email = log.email.data
            password = log.password.data
            scoutdeets = Scout.query.filter(Scout.email==email).first()
            if scoutdeets:
                stored_password = scoutdeets.scout_password_hash
                check = check_password_hash(stored_password,password)
                if check == True:
                    session["useronline"] = scoutdeets.scout_firstname
                    session["userid"] = scoutdeets.scout_id
                    session["usertype"] = "scout"
                    return redirect(url_for('scout_profile'))
                else:
                    flash("Invalid credentials",category="danger")
                    return redirect(url_for('scout_login'))
            else:
                flash("Invalid credentials",category="danger")
                return redirect(url_for('scout_login'))
        else:
            return render_template("user/login.html",log=log)
        




@app.get('/logout/')
def logout():
    if session.get('useronline') and session.get('userid'):
        session.pop('useronline',None)
        session.pop('userid',None)
        session.clear()
    return redirect(url_for('home'))





@app.route('/profile/',methods=["GET","POST"])
def profile():
    photoform = PhotoForm()
    if session.get('usertype')== 'player' and session.get('userid'):
        userdeets = Player.query.get(session['userid'])
        if request.method == 'GET':
            return render_template('user/profile.html',userdeets=userdeets,photoform=photoform)
        else:
            flash("please login here to continue",category="danger")
            return render_template('user/login.html',photoform=photoform,userdeets=userdeets)
    else:
        flash('You need to log in as a player',category='danger')
        return redirect(url_for('player_login'))
    


@app.route('/profile/<id>/')
def featured_players(id):
    log = Login()
    play = Player.query.get(id)
    userdeets = db.session.query(Player).first()
    if session.get("userid") or session.get("adminid") and session.get("useronline") or session.get("adminonline"):
        return render_template('user/featured_players.html',play=play,userdeets=userdeets,log=log)
    else:
        flash("You need to login to view player details",category="danger")
        return redirect(url_for('scout_login'))
        


@app.route('/players/')
def players():
    play = Player.query.all()
    return render_template('user/players.html',play=play)



    

@app.route('/profile/scout/',methods=["GET","POST"])
def scout_profile():
    if session.get('usertype')== 'scout' and session.get('userid'):
        userdeets = Scout.query.get(session['userid'])
        if request.method == 'GET':
            return render_template('user/scout_profile.html',userdeets=userdeets)
        else:
            flash("please login here to continue",category="danger")
            return render_template('user/login.html',userdeets=userdeets)
    else:
        flash('You need to log in as a scout',category='danger')
        return redirect(url_for('scout_login'))




@app.route('/search/')
def search_view():
    name = request.args.get('name')
    position = request.args.get('position')
    sortage = request.args.get('age')
    query = Player.query
    if name:
        query = query.filter(or_((Player.player_firstname).ilike(f'%{name}%'),
                             (Player.player_lastname).ilike(f'%{name}%')
                             ))
    if position:
        query = query.join(Position).filter(Position.position_name == position)
    if sortage == "age":
        query = query.order_by(Player.player_date_of_birth.desc())
    play = query.all()
    return render_template("user/player_card.html",play=play)






@app.route('/profile/edit',methods=['GET','POST'])
def profile_edit():
    prof = Profileform()
    photoform = PhotoForm()
    userdeets = Player.query.get(session['userid'])
    vid = userdeets.videos[0] if userdeets.videos else None
    if session.get('usertype') != 'player':
        flash('You need to log in as a player to access this page')
        return redirect(url_for('home'))
    else:
        if (session.get('usertype') in ['scout', 'admin']) and session.get('userid') or session.get('adminid'):
            userdeets = Player.query.get(session['userid'])
            if request.method == 'GET':
                if vid:
                    prof.video_caption.data = vid.video_caption
                    prof.video_link.data = vid.video_link
                    prof.video_description.data = vid.video_description
                else:
                    prof.video_caption.data = ''
                    prof.video_link.data = ''
                    prof.video_description.data = ''
                return render_template('user/profile_edit.html',prof=prof,userdeets=userdeets,photoform=photoform,vid=vid)
            else:
                if prof.validate_on_submit():
                    firstname = prof.firstname.data
                    lastname = prof.lastname.data
                    phone = prof.phone_number.data
                    dob = prof.dob.data
                    video_caption = prof.video_caption.data
                    video_link = prof.video_link.data
                    video_description = prof.video_description.data
                    userdeets.player_firstname = firstname
                    userdeets.player_lastname = lastname
                    userdeets.player_phone = phone
                    userdeets.player_date_of_birth = dob
                    if video_link:
                        vid.video_link = video_link
                        vid.video_description = video_description
                        vid.video_caption = video_caption
                    else:
                        video = Video(
                            video_link = video_link,
                            player_id = session.get('userid'),
                            video_description = video_description,
                            video_caption = video_caption
                        )
                        db.session.add(video)
                        db.session.commit()
                    db.session.commit()
                    session['useronline'] = prof.firstname.data  #also change the name in the session
                    flash("Profile successfully updated",category="success")
                    return redirect(url_for('profile_edit'))
                else:
                    # prof.summary.data = userdeets.usr_summary
                    return render_template('user/profile_edit.html',prof=prof,userdeets=userdeets,photoform=photoform,vid=vid)
        else:
            flash("Please login to continue",category='danger')
            return redirect(url_for('player_login'))
    





@app.route("/profile/picture/",methods=["POST",'GET'])
def profile_picture():
    photoform = PhotoForm()
    if session.get('userid') and session.get('useronline'):
        if request.method == 'POST' and photoform.validate_on_submit():
            #retrieve formdata and upload
            photo_obj = photoform.photo.data
            dfilename = photo_obj.filename
            name,extension = os.path.splitext(dfilename)
            newname = secrets.token_hex(10) + extension      # *10 means how many bits(length of the filename)
            photo_obj.save('pkg/static/uploads/'+newname)       #saved the photo with a random name generated
            #save in db for user that is logged in
            player = Player.query.get(session['userid'])
            player.player_photo = newname
            db.session.commit()
            flash("Photo uploaded",category="success")
            return redirect(url_for('profile_edit'))
        else:
            flash("Filetype not allowed")
            return redirect(url_for('profile_edit'))
    else:
        flash("Please login to continue",category='danger')
        return redirect(url_for('player_login'))





@app.route('/scout/profile/edit',methods=['GET','POST'])
def scout_profile_edit():
    proff = ScoutProfileform()
    photof = PhotoForm()
    if session.get('usertype') != 'scout':
        flash('You need to log in as a scout to access this page')
        return redirect(url_for('home'))
    else:
        if (session.get('usertype') in ['scout', 'admin']) and session.get('userid'):
            userdeetss = Scout.query.get(session['userid'])
            if request.method == 'GET':
                return render_template('user/scout_profile_edit.html',proff=proff,userdeetss=userdeetss,photof=photof)
            else:
                if proff.validate_on_submit():
                    firstname = proff.firstname.data
                    lastname = proff.lastname.data
                    userdeetss.scout_firstname = firstname
                    userdeetss.scout_lastname = lastname
                    db.session.commit()
                    session['useronline'] = proff.firstname.data
                    flash("Profile successfully updated",category="success")
                    return redirect(url_for('scout_profile_edit'))
                else:
                    return render_template('user/scout_profile_edit.html',proff=proff,userdeetss=userdeetss,photof=photof)
        else:
            flash("Please login to continue",category='danger')
            return redirect(url_for('scout_login'))
    



@app.route("/scout/profile/picture/",methods=["POST",'GET'])
def scout_profile_picture():
    photof = PhotoForm()
    if session.get('userid') and session.get('useronline'):
        if request.method == 'POST' and photof.validate_on_submit():
            photo_obj = photof.photo.data
            dfilename = photo_obj.filename
            name,extension = os.path.splitext(dfilename)
            newname = secrets.token_hex(10) + extension
            photo_obj.save('pkg/static/uploads/'+newname)
            scout = Scout.query.get(session['userid'])
            scout.scout_photo = newname
            db.session.commit()
            flash("Photo uploaded",category="success")
            return redirect(url_for('scout_profile_edit'))
        else:
            flash("Filetype not allowed")
            return redirect(url_for('scout_profile_edit'))
    else:
        flash("Please login to continue",category='danger')
        return redirect(url_for('scout_login'))


@app.route('/faq/')
def faq():
    return render_template('user/faq.html')

@app.route('/terms/')
def terms():
    return render_template('user/terms_&_conditions.html')






@app.route('/insert-positions/')
def insert_positions():
    p1 = Position(position_name="Striker(ST)")
    p2 = Position(position_name="Left Winger(LW)")
    p3 = Position(position_name="Right Winger(RW)")
    p4 = Position(position_name="Central Midfielder(CM)")
    p5 = Position(position_name="Central Attacking Midfielder(CAM)")
    p6 = Position(position_name="Center Back(CB)")
    p7 = Position(position_name="Left Back(LB)")
    p8 = Position(position_name="Right Back(RB)")
    p9 = Position(position_name="Goalkeeper(GK)")
    db.session.add_all([p1,p2,p3,p4,p5,p6,p7,p8,p9])
    db.session.commit()
    return "Positions inserted successfully!"





# @app.get('/configitems/')
# def configitems():
#     items = app.config
#     print(app.config.get('SECRET_KEY'))
#     return render_template('user/config.html',items=items)


# @app.route('/addcountries/')
# def add_countries():
#     countries = [
#         "Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia",
#         "Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium",
#         "Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei",
#         "Bulgaria","Burkina Faso","Burundi","Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic",
#         "Chad","Chile","China","Colombia","Comoros","Congo (Brazzaville)","Congo (Kinshasa)","Costa Rica",
#         "Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic",
#         "Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia",
#         "Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada",
#         "Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India",
#         "Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan",
#         "Kenya","Kiribati","Korea, North","Korea, South","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia",
#         "Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar","Malawi",
#         "Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia",
#         "Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal",
#         "Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan",
#         "Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal",
#         "Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines",
#         "Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone",
#         "Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain",
#         "Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania",
#         "Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan",
#         "Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay",
#         "Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"
#     ]

#     country_objects = [Country(country_name=c) for c in countries]
#     db.session.add_all(country_objects)
#     db.session.commit()

#     return("All countries added successfully!")