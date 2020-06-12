from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.trailer import Trailer

def new():
    return render_template("trailers/new.html")

def create(): #Crea / Guarda un archivo de libro
    set_db()
    if validate_book_isbn(isbn) and not Book.is_complete(isbn):    
        if request.files: 
            archivo = request.files['archivo']
            book_name = Book.find_meta_by_isbn(isbn)['titulo']  
            if not os.path.exists('flaskps/static/uploads/'+book_name):          
                os.mkdir('flaskps/static/uploads/'+book_name)        
            archivo.save(os.path.join('flaskps/static/uploads/_trailers'+book_name, book_name+"_Full.pdf"))
        Book.create(request.form, book_name+"_Full.pdf",isbn)
        Book.mark_complete(isbn)
        print(Book.is_complete(isbn))
        flash("Libro cargado")
    else:
        flash("Ya existe un libro con el mismo ISBN")
    return redirect(url_for("book_menu"))
"""
def index():
    set_db()
    #novedades = Novedad.all()
    #admPermit = "configuracion_usarInhabilitado" in session['permisos']
    return render_template("novedad/menu.html")#, novedades=novedades, adm=admPermit)


"""
def set_db():
    Trailer.db = get_db()