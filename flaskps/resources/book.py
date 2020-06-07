from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.book import Book
from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero

import datetime as dt
import os

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
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('books/menu.html', books=books, i=i, pag=pag, adm=adm)

#creacion de libros
def new(isbn):
    set_db()
    titulo = Book.find_meta_by_isbn(isbn)['titulo']
    today = dt.datetime.now().strftime("%Y-%m-%d")
    return render_template('books/new.html', isbn=isbn, titulo=titulo, today=today)

def create(isbn):
    set_db()
    if validate_book_isbn(isbn) and not Book.is_complete(isbn):    
        if request.files: 
            archivo = request.files['archivo']
            book_name = Book.find_meta_by_isbn(isbn)['titulo']  
            if not os.path.exists('flaskps/static/uploads/'+book_name):          
                os.mkdir('flaskps/static/uploads/'+book_name)        
            archivo.save(os.path.join('flaskps/static/uploads/'+book_name, book_name+"_Full"))
        Book.create(request.form, book_name+"_Full",isbn)
        Book.mark_complete(isbn)
        print(Book.is_complete(isbn))
        flash("Libro cargado")
    else:
        flash("Ya existe un libro con el mismo ISBN")
    return redirect(url_for("book_menu"))

#Creacion de capitulo
def new_chapter(isbn):
    set_db()
    titulo = Book.find_meta_by_isbn(isbn)['titulo']
    today = dt.datetime.now().strftime("%Y-%m-%d")
    return render_template('books/new_chapter.html', isbn=isbn, titulo=titulo, today=today)

def create_chapter(isbn):
    set_db()
    print("Crea cap")
    if not Book.is_complete(isbn):    
        if request.files: 
            archivo = request.files['archivo']
            book_name = Book.find_meta_by_isbn(isbn)['titulo']
            chapter_name = book_name + "_cap_"+str(request.form['num'])
            if not os.path.exists('flaskps/static/uploads/'+book_name):
                os.mkdir('flaskps/static/uploads/'+book_name)            
            if validate_chapter_isbn(isbn, request.form['num']):
                archivo.save(os.path.join('flaskps/static/uploads/', chapter_name))
                Book.create_chapter(request.form, chapter_name,isbn)
            else:
                flash("El capitulo  ya fue cargado")#+str(request.form['num']+
                return redirect(url_for("book_menu"))
        
        if request.form['completo']=="True":            
            Book.mark_complete(isbn)
        
        flash("Capitulo cargado")
    else:
        flash("Ya se cargo todo el libro")
    print("Hizo todo")
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
    if validate_meta_isbn(request.form['isbn']):
        
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
    book['autor'] = Autor.find_by_id(book['autor_id'])['nombre']
    book['editorial'] = Editorial.find_by_id(book['editorial_id'])['nombre']
    book['genero'] = Genero.find_by_id(book['genero_id'])['nombre']
    print(book)
    return render_template('books/edit_meta.html',book=book, isbn=isbn, autores=autores, editoriales=editoriales, generos=generos)

def load_edit_meta(isbn):
    set_db()
    
    book = Book.find_meta_by_isbn(isbn)
    
    book_data = {}
    
    book_data['titulo'] = request.form.get('titulo') if (request.form.get('titulo') != '') else book['titulo']
    book_data['sinopsis'] = request.form.get('sinopsis') if (request.form.get('sinopsis') != '') else book['sinopsis']
    if request.form.get('autor') != '':
        print("se carga lo ingresado")
        autor = Autor.find_by_name(request.form['autor'])
        if autor == None:
            new_autor =request.form['autor']
            Autor.create({'nombre':new_autor})
            autor_id = Autor.find_by_name(new_autor)['id']
        else:
            autor_id = autor['id']
    else:
        print("Se carga lo previo")
        autor_id = book['autor_id']

    if request.form.get('editorial') != '':
        print("se carga lo ingresado")
        editorial = Editorial.find_by_name(request.form['editorial'])
        if editorial == None:
            new_Editorial =request.form['editorial']
            Editorial.create({'nombre':new_Editorial})
            Editorial_id = Editorial.find_by_name(new_Editorial)['id']
        else:
            Editorial_id = editorial['id']
    else:
        print("Se carga lo previo")
        Editorial_id = book['editorial_id']

    if request.form.get('genero') != '':
        print("se carga lo previo")
        genero = Genero.find_by_name(request.form['genero'])
        if genero == None:
            new_Genero =request.form['genero']
            Genero.create({'nombre':new_Genero})
            Genero_id = Genero.find_by_name(new_Genero)['id']
        else:            
            Genero_id = genero['id']
    else:
        print("Se carga lo previo")
        Genero_id = book['genero_id']    
    modified = False
    for key in request.form.keys():
        if (request.form.get(key) != ''):
            modified = True
            break    
    Book.updateMeta(book_data, isbn, autor_id, Editorial_id, Genero_id)
    if modified:
        flash("Datos modificados correctamente")
    else: 
        flash("No se Ingresó ningún dato, no se modifcó el metadato")
    
    return redirect(url_for("book_menu"))
    

def remove_meta(isbn):
    set_db()
    Book.deleteMeta(isbn)
    return redirect(url_for("book_menu"))
#Muestra de libros

def open_book():
    return render_template('books/abrirlibro.html')

def validate_meta_isbn(isbn):
    book = Book.find_meta_by_isbn(isbn)
    return book == None

def validate_book_isbn(isbn):
    book = Book.find_by_isbn(isbn)
    return book == None

def validate_chapter_isbn(isbn, num):
    book = Book.find_chapter_by_isbn(isbn, num)
    return book == None

def set_db():
    Book.db = get_db()
    Autor.db = get_db()
    Editorial.db = get_db()
    Genero.db = get_db()