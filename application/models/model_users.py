import web
import app

db = app.db

def validate_user(user):
    try:
        return db.select('users', where='user=$user', vars=locals())[0]
    except Exception as e:
        print(("Model get all Error {}".format(e.args)))
        print(("Model get all Message {}".format(e.message)))
        return None

def get_all_users():
    try:
        return db.select('users') 
    except Exception as e:
        print(("Model get all Error {}".format(e.args)))
        print(("Model get all Message {}".format(e.message)))
        return None

def get_picture(user):
    try:
        return db.select('users',what="picture", where= 'user = $user', vars=locals())[0] #selecciona el primer registro que coincida con el nombre
    except Exception as e:
        print "Model get_picture Error ()",format(e.args)
        print "Model get_picture Message {}",format(e.message)
        return None

def get_users(user):
    try:
        return db.select('users', where='user=$user', vars=locals())[0] 
    except Exception as e:
        print(("Model get Error {}".format(e.args)))
        print(("Model get Message {}".format(e.message)))
        return None

def get_nombre(user):
    try:
        return db.select('users',what="nombre", where= 'user = $user', vars=locals())[0] #selecciona el primer registro que coincida con el nombre
    except Exception as e:
        print "Model get_nombre Error ()",format(e.args)
        print "Model get_nombre Message {}",format(e.message)
        return None

def edit_grado(user,grado):
    try:
        return db.update('users',
            user=user,
            grado=grado,
            where='user=$user',
            vars=locals())
    except Exception as e:
        print("Model update Error {}".format(e.args))
        print("Model updateMessage {}".format(e.message))
        return None

def insert_users(correo,nombre,carrera,grado,tipo):
    try:
        return db.insert('users',
        user=correo,
        nombre=nombre,
        carrera=carrera,
        grado=grado,
        tipo=tipo)
    except Exception as e:
        print "Model insert Error {}".format(e.args)
        print "Model insert Message {}".format(e.message)
        return None