from app import app
from flask import render_template,request,redirect, flash
from .models import db, ServiceCategory,ServiceProfessional,User,Admin,ServicePackage
from flask_login import login_user , login_required , current_user

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login" , methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # first logic
        u= db.session.query(Admin).filter_by(email=email).first() or \
            db.session.query(ServiceProfessional).filter_by(email=email).first() or \
                db.session.query(User).filter_by(email=email).first()
        if u :
            if u.password == password:
                if isinstance(u , Admin):
                    login_user(u)
                    return redirect(f"/admin/dashboard")
                elif isinstance(u , ServiceProfessional):
                    login_user(u)
                    return redirect(f"/professional/dashboard")
                elif isinstance(u, User):
                    login_user(u)
                    return redirect(f"/customer/dashboard")
            
            else:
                flash("Incorrect password")
                return redirect("/login")

        else:
            flash("email doesn't exist")
            return redirect("/login")
            


        #####2nd logic

        # role = request.form.get("role")
        # print(role)
        # if role =="admin":
        #     admin = db.session.query(Admin).filter_by(email=email).first()
        #     if admin:
        #         if admin.password == password:
        #             return redirect("/admin/dashboard")
        #         else:
        #             return "Incorrect Password"
        #     else:
        #         "provide correct email for admin"
        # elif role =="customer":
        #     cust = db.session.query(User).filter_by(email=email).first()
        #     if cust:
        #         if cust.password == password:
        #             return redirect("/customer/dashboard")
        #         else:
        #             return "Incorrect Password"
        #     else:
        #         return "provide correct email for customer"
        # elif role =="professional":
        #     prof = db.session.query(ServiceProfessional).filter_by(email=email).first()
        #     if prof:
        #         if prof.password == password:
        #             return redirect("/professional/dashboard")
        #         else:
        #             return "Incorrect Password"
        #     else:
        #         return "provide correct email for professional" 




@app.route("/register" , methods=["GET" ,"POST"])
def register():
    if request.method=="GET":
        if request.args.get("u_type") =="professional":
            cats = db.session.query(ServiceCategory).all()
            return render_template("/professional/register.html" , categories =cats)
        elif request.args.get("u_type") =="customer":
            return render_template("/customer/register.html")
    elif request.method=="POST":
        if request.args.get("u_type") =="professional":
            p_name = request.form.get("prof_name")
            p_email = request.form.get("prof_email")
            p_password = request.form.get("prof_password")
            p_city = request.form.get("prof_city")
            p_phone = request.form.get("prof_phone")
            cat = request.form.get("prof_category")
            
            prof = db.session.query(ServiceProfessional).filter_by(email=p_email).first()
            if not prof:
                prof = ServiceProfessional(name=p_name,email=p_email, password=p_password,status="Requested" , city=p_city,phone=p_phone,cat_id=cat)
                db.session.add(prof)
                db.session.commit()
                return redirect("/login")
            else:
                flash("email already exist for professional")
                return redirect("/register?u_type=professional")
        elif request.args.get("u_type") =="customer":
            c_name = request.form.get("cust_name")
            c_email = request.form.get("cust_email")
            c_password = request.form.get("cust_password")
            c_city = request.form.get("cust_city")
            c_phone = request.form.get("cust_phone")
            c_address = request.form.get("cust_address")
            cust = db.session.query(User).filter_by(email=c_email).first()
            if not cust:
                cust = User(name=c_name,email=c_email, password=c_password,status="Active", city=c_city,phone=c_phone,address=c_address)
                db.session.add(cust)
                db.session.commit()
                return redirect("/login")
            else:
                flash("email already exist for customer")
                return redirect("/register?u_type=customer")
        
        



@app.route("/admin/dashboard" , methods=["GET" , "POST"])
@login_required
def admin_dashboard():
    cats = db.session.query(ServiceCategory).all()
    active_prof = db.session.query(ServiceProfessional).filter_by(status="Active").all()
    requested_prof = db.session.query(ServiceProfessional).filter_by(status="Requested").all()
    flagged_prof = db.session.query(ServiceProfessional).filter_by(status="Flagged").all()
    active_cust = db.session.query(User).filter_by(status="Active").all()
    flagged_cust = db.session.query(User).filter_by(status="Flagged").all()

    return render_template("/admin/dashboard.html" , current_admin = current_user , all_cats = cats,
                           active_prof = active_prof, requested_prof=requested_prof, flagged_prof=flagged_prof,
                            active_cust=active_cust, flagged_cust=flagged_cust ) 



@app.route("/professional/dashboard" , methods=["GET" , "POST"])
@login_required
def prf_dashboard():
    
    return render_template("/professional/dashboard.html" , current_professional = current_user) 
    


@app.route("/customer/dashboard" , methods=["GET" , "POST"])
@login_required
def cust_dashboard():

    return render_template("/customer/dashboard.html" , current_cust = current_user) 



@app.route("/professional/stats")
def prof_stats():
    if request.args.get("u_id"):
        prof = db.session.query(ServiceProfessional).filter_by(id = request.args.get("u_id")).first()
        return f"welcome to {prof.name} stats page"
    


@app.route("/category" , methods=["POST"])
def category():
    if request.args.get("task") =="create":
        name = request.form.get("cat_name")
        cat = db.session.query(ServiceCategory).filter_by(name=name).first()
        if cat:
            flash("Category already exist")
            return redirect("/admin/dashboard")
        
        else:
            new_cat = ServiceCategory(name=name)
            db.session.add(new_cat)
            db.session.commit()
            flash("Category is created")
            return redirect("/admin/dashboard")
    elif request.args.get("task") == "edit":
        name = request.form.get("cat_name")
        cat_id = request.args.get("cat_id")
        cat = db.session.query(ServiceCategory).filter_by(id = cat_id).first()
        if cat:
            if name:
                cat.name = name
                
            db.session.commit()
            flash("category is updated")
            return redirect("/admin/dashboard")

        else:
            flash("category doesn't exist.")
            return redirect("/admin/dashboard")




@app.route("/professional" , methods=["POST"])
def pofessional():
    if request.args.get("task") =="accept":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status="Active"
            db.session.commit()
            flash(f"{prof.name}'s request is accepted ")
            return redirect("/admin/dashboard")
    elif request.args.get("task") =="reject":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status="Rejected"
            db.session.commit()
            flash(f"{prof.name}'s request is Rejected")
            return redirect("/admin/dashboard")
    elif request.args.get("task") =="flag":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status="Flagged"
            db.session.commit()
            flash(f"{prof.name} is flagged ")
            return redirect("/admin/dashboard")
    elif request.args.get("task") =="unflag":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status="Active"
            db.session.commit()
            flash(f"{prof.name} is unflagged ")
            return redirect("/admin/dashboard")



@app.route("/customer" , methods=["POST"])
def customer():
    
    
    if request.args.get("task") =="flag":
        cust_id = request.args.get("cust_id")
        cust = db.session.query(User).filter_by(id = cust_id).first()
        if cust:
            cust.status="Flagged"
            db.session.commit()
            flash(f"{cust.name} is flagged ")            
            return redirect("/admin/dashboard")
    elif request.args.get("task") =="unflag":
        cust_id = request.args.get("cust_id")
        cust = db.session.query(User).filter_by(id = cust_id).first()
        if cust:
            cust.status="Active"
            db.session.commit()
            flash(f"{cust.name} is unflagged ")
            return redirect("/admin/dashboard")    
    
    


@app.route("/package" , methods=["POST"])
def package():
    if request.args.get("task") == "create":
        pack_name = request.form.get("pack_name")
        pack_price= request.form.get("pack_price")
        print(pack_name)
        new_pack = ServicePackage(name=pack_name , price=pack_price ,prof_id = current_user.id , cat_id = current_user.category.id )
        db.session.add(new_pack)
        db.session.commit()
        flash("Package is created")
        return redirect("/professional/dashboard")
    elif request.args.get("task") == "edit":
        pack_name = request.form.get("pack_name")
        pack_price= request.form.get("pack_price")
        pack_id = request.args.get("pack_id")
        pack  = db.session.query(ServicePackage).filter_by(id = pack_id).first()
        if pack : 
            if pack_name:
                pack.name = pack_name
            if pack_price:
                pack.price = pack_price
            db.session.commit()
        
            flash("Package is updated")
            return redirect("/professional/dashboard")
