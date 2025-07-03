from .models import db,Admin,ServiceCategory,ServiceProfessional



if db.session.query(Admin).count()==0:
    admin = Admin(name="admin" , email = "admin@myapp.com" , password="pass")
    db.session.add(admin)
    db.session.commit()

if db.session.query(ServiceCategory).count()==0:
    homecleaning = ServiceCategory(name="Home Cleaning")
    db.session.add(homecleaning)

    Gardening = ServiceCategory(name="Gardening")
    db.session.add(Gardening)
    db.session.commit()

if db.session.query(ServiceProfessional).count()==0:
    
    R = ServiceProfessional(name="Ram" , email = "Ram@myapp.com" ,password="pass" , city = "Jaipur" , phone="9999999999",cat_id=2 )
    db.session.add(R)
    S = ServiceProfessional(name="Shyam" , email = "Shyam@myapp.com" ,password="pass" , city = "Delhi" , phone="9999999999",cat_id=2 )

    db.session.add(S)

    P = ServiceProfessional(name="Prakash" , email = "Prakash@myapp.com" ,password="pass" , city = "Delhi" , phone="9999999999",cat_id=1 )
    db.session.add(P)
    db.session.commit()




