from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.book import Book
from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero


def render_menu():
    set_db()
    books = Book.allMeta()    
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(books)):
        i = i - 1
    return render_template('books/menu.html', books=books, i=i, pag=pag)

#creacion de libros
def new():
    return render_template('books/new.html')

def create():
    set_db()
    if validate_isbn(request.form['isbn']):
        Book.create(request.form)
        flash("Libro cargado")
    else:
        flash("Ya existe un libro con el mismo ISBN")
    return redirect(url_for("book_menu"))

#crud de metadatos
def render_meta():
    set_db()
    autores = list(map(lambda autor: autor['nombre'],Autor.all()))
    editoriales = list(map(lambda editorial: editorial['nombre'],Editorial.all()))
    generos = list(map(lambda genero: genero['nombre'],Genero.all()))
    return render_template('books/new_meta.html', autores=autores, editoriales=editoriales, generos=generos)

def load_meta():
    set_db()
    
    autor = Autor.find_by_name(request.form['autor'])
    if autor == None:
        new_autor =request.form['autor']
        Autor.create({'nombre':new_autor})
        autor_id = Autor.find_by_name(new_autor)['id']
    else:
        autor_id = autor['id']

    editorial = Editorial.find_by_name(request.form['editorial'])

    if editorial == None:
        new_Editorial =request.form['editorial']
        Editorial.create({'nombre':new_Editorial})
        Editorial_id = Editorial.find_by_name(new_Editorial)['id']
    else:
        Editorial_id = editorial['id']

    genero = Genero.find_by_name(request.form['genero'])
    if genero == None:
        new_Genero =request.form['genero']
        Genero.create({'nombre':new_Genero})
        Genero_id = Genero.find_by_name(new_Genero)['id']
    else:
        Genero_id = genero['id']    
    if validate_isbn(request.form['isbn']):
        
        Book.loadMeta(request.form, autor_id, Editorial_id, Genero_id)
        flash("Metadatos cargados")
    else:
        flash("Ya existe un libro con el mismo ISBN")
        return redirect(url_for("book_meta"))
    
    
    return redirect(url_for("book_menu"))

def edit_meta(isbn):
    set_db()
    autores = Autor.all()
    editoriales = Editorial.all()
    generos = Genero.all()
    book=Book.find_meta_by_isbn(isbn)    
    return render_template('books/edit_meta.html',book=book, isbn=isbn, autores=autores, editoriales=editoriales, generos=generos)

def load_edit_meta(isbn):
    set_db()

    autor = Autor.find_by_name(request.form['autor'])
    if autor == None:
        new_autor =request.form['autor']
        Autor.create({'nombre':new_autor})
        autor_id = Autor.find_by_name(new_autor)['id']
    else:
        autor_id = autor['id']

    editorial = Editorial.find_by_name(request.form['editorial'])

    if editorial == None:
        new_Editorial =request.form['editorial']
        Editorial.create({'nombre':new_Editorial})
        Editorial_id = Editorial.find_by_name(new_Editorial)['id']
    else:
        Editorial_id = editorial['id']

    genero = Genero.find_by_name(request.form['genero'])
    if genero == None:
        new_Genero =request.form['genero']
        Genero.create({'nombre':new_Genero})
        Genero_id = Genero.find_by_name(new_Genero)['id']
    else:
        Genero_id = genero['id']
    
    Book.updateMeta(request.form, isbn, autor_id, Editorial_id, Genero_id)
    return redirect(url_for("book_menu"))

def remove_meta(isbn):
    set_db()
    Book.deleteMeta(isbn)
    return redirect(url_for("book_menu"))
#Muestra de libros

def validate_isbn(isbn):
    book = Book.find_meta_by_isbn(isbn)
    print(book)
    print(book == None)
    return book == None

def set_db():
    Book.db = get_db()
    Autor.db = get_db()
    Editorial.db = get_db()
    Genero.db = get_db()