import config as config
import web
import app


class Evaluar():

    def __init__(self):
        pass

    def GET(self,num_as):
        app.session.num_as = num_as
        asesoria = config.model_asesoria.get_asesorias(num_as)
        nombre = config.model_users.get_nombre(asesoria.solicitante)
        return config.render.evaluacion_asesor(asesoria,nombre.nombre) # render evaluacion_asesor.html

    def POST(self,num_as):
        formulario = web.input() # get form data
        horas = formulario['horas']
        asistencia = formulario['asistencia']
        observaciones = formulario['observaciones']
        calificacion = formulario['calificacion']
        extra = formulario['extra']
        estado = 'calificado'
        asesoria = app.session.num_as
        config.model_evaluacion_alumno.insert_evaluacion_alumno(asesoria,horas,asistencia,observaciones,calificacion,extra)
        evaluacion = config.model_evaluacion_asesor.asesor_evaluado(asesoria)
        print "evaluacion: ",evaluacion 
        if evaluacion == 1:
            config.model_asesoria.update_asesoria(asesoria,estado)
            raise web.seeother('/index_asesoria') # redirecciona el HTML
        else:
            raise web.seeother('/index_asesoria') # redirecciona el HTML