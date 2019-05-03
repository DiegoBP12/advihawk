# -*- coding:utf-8 -*-
import config as config
import web
import app
import hashlib


class Insert():

    def __init__(self):
        pass

    def GET(self):
        user =  app.session.user
        message = "Por favor regístrate para poder hacer uso de la plataforma" 
        return config.render.registro(user,message) # render insert.html

    def POST(self):
        formulario = web.input() # get form data
        # call model insert_registro and try to insert new data
        correo = formulario['user']
        nombre= formulario['nombre']
        carrera = formulario['carrera']
        grado = formulario['grado']
        tipo = formulario['tipo']
        correcto = False
        if '@utectulancingo.edu.mx' in correo:
            correcto = True
        else:
            web.setcookie('_id', '', 0)  # cierre de session en google
            raise web.seeother('/') # render registro index.html
        user_hash = hashlib.md5(correo + app.secret_key).hexdigest() # encrypt user_hash
        picture = app.session.picture
        print tipo
        if tipo == '0' and correcto == True:
            config.model_registro.insert_registro(correo,nombre,carrera,grado,tipo,user_hash,picture)
            config.model_asesor.insert_asesor(correo,nombre,carrera,grado)
        elif correcto == True:
            config.model_registro.insert_registro(correo,nombre,carrera,grado,tipo,user_hash,picture)
        raise web.seeother('/') # render registro index.html