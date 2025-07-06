from app import app
from flask import render_template,request,redirect
from .models import db, ServiceCategory,ServiceProfessional,User,Admin
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
                return "Incorrect Password"

        else:
            return "email doesn't exist"


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
                prof = ServiceProfessional(name=p_name,email=p_email, password=p_password,city=p_city,phone=p_phone,cat_id=cat)
                db.session.add(prof)
                db.session.commit()
                return redirect("/login")
            else:
                return "email already exist for professional"
        elif request.args.get("u_type") =="customer":
            c_name = request.form.get("cust_name")
            c_email = request.form.get("cust_email")
            c_password = request.form.get("cust_password")
            c_city = request.form.get("cust_city")
            c_phone = request.form.get("cust_phone")
            c_address = request.form.get("cust_address")
            cust = db.session.query(User).filter_by(email=c_email).first()
            if not cust:
                cust = User(name=c_name,email=c_email, password=c_password,city=c_city,phone=c_phone,address=c_address)
                db.session.add(cust)
                db.session.commit()
                return redirect("/login")
            else:
                return "email already exist for customer"
        
        



@app.route("/admin/dashboard" , methods=["GET" , "POST"])
@login_required
def admin_dashboard():
    
    
    return render_template("/admin/dashboard.html" , current_admin = current_user) 



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