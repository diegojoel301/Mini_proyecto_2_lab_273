# -*- coding: utf-8 -*-
import socket
import sqlite3
from urllib.parse import parse_qs, urlparse, unquote_plus
def create_table():
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Creación de tabla alumno si no existe
    conn.execute('''CREATE TABLE IF NOT EXISTS alumno
                     (CI INT PRIMARY KEY NOT NULL,
                         Nombre TEXT NOT NULL,
                         Apellido TEXT NOT NULL,
                         fecha_nac DATE NOT NULL);''')
    #asignatura
    conn.execute('''CREATE TABLE IF NOT EXISTS asignatura
                     (Sigla TEXT PRIMARY KEY NOT NULL,
             Nombre TEXT NOT NULL,
             Semestre TEXT NOT NULL);''')
    #alumno_asignatura
    conn.execute('''CREATE TABLE IF NOT EXISTS alumno_asignatura
                      (Ci INT NOT NULL,
             Sigla TEXT NOT NULL,
             nota1 FLOAT,
             nota2 FLOAT,
             notafinal FLOAT,
             PRIMARY KEY (Ci, Sigla),
             FOREIGN KEY (Ci) REFERENCES alumno(CI),
             FOREIGN KEY (Sigla) REFERENCES asignatura(Sigla));''')
    # Cerramos la conexión
    conn.close()
#mostrar tabla alumno

def select_alumnos():
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todos los alumnos
    cursor = conn.execute('SELECT * FROM alumno')

    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>CI</th><th>Nombre</th><th>Apellido</th><th>Fecha de nacimiento</th><th>Acciones</th></tr>'
    for row in cursor:
        ci = row[0]
        html += f'<tr><td>{ci}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td>'
        html += f'<td><a href="editar_alumno?Ci={ci}&Nombre={row[1]}&Apellido={row[2]}&fecha_nac={row[3]}" class="btn btn-success">Editar</a>&ensp;<a href="eliminar_alumno?ci={ci}" class="btn btn-danger">Eliminar</a>&ensp;<a href="inscribir_estudiante?ci={ci}&nombre={row[1]}&apellido={row[2]}" class="btn btn-warning">Inscribir Asignatura</a></td></tr>'
        
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html

#mostrar asignaturas
def select_asignatura():
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todas las asignaturas
    cursor = conn.execute('SELECT * FROM asignatura')

    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>Sigla</th><th>Nombre</th><th>Semestre</th><th>Acciones</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td>'
        html += f'<td><a href="editar_asignatura?Sigla={row[0]}&Nombre={row[1]}&Semestre={row[2]}" class="btn btn-success">Editar</a></td>'
        html += f'<td><a href="eliminar_asignatura?sigla={row[0]}" class="btn btn-danger">Eliminar</a></td></tr>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html



def insert_alumno(Ci, Nombre, Apellido, fecha_nac):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Inserción de contacto
    conn.execute(f"INSERT INTO alumno (CI, Nombre, Apellido, fecha_nac) \
                    VALUES ('{Ci}', '{Nombre}', '{Apellido}','{fecha_nac}');")

    # Guardamos los cambios
    conn.commit()

    # Cerramos la conexión
    conn.close()

def insert_asignatura(Sigla, Nombre, Semestre):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Inserción de contacto
    conn.execute(f"INSERT INTO asignatura (Sigla, Nombre, Semestre) VALUES ('{Sigla}', '{Nombre}', '{Semestre}');")

    # Guardamos los cambios
    conn.commit()

    # Cerramos la conexión
    conn.close()


def eliminar_alumno(id):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Eliminamos el registro correspondiente
    conn.execute(f"DELETE FROM alumno WHERE CI='{id}'")
    conn.execute(f"DELETE FROM alumno_asignatura WHERE Ci='{id}'")

    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def editar_alumno(ci, nombre, apellido, fecha_nac):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Eliminamos el registro correspondiente
    conn.execute(f"UPDATE alumno SET Nombre='{nombre}', Apellido='{apellido}', fecha_nac='{fecha_nac}' WHERE CI='{ci}'")

    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def eliminar_asignatura(sigla):
     # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Eliminamos el registro correspondiente
    conn.execute(f"DELETE FROM asignatura WHERE Sigla='{sigla}'")
    conn.execute(f"DELETE FROM alumno_asignatura WHERE Sigla='{sigla}'")

    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def actualizar_asignatura(sigla, nombre, semestre):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    conn.execute(f'UPDATE asignatura SET Nombre = "{nombre}", Semestre = "{semestre}" WHERE Sigla LIKE "{sigla}"')
    
    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def select_asignatura_estudiante():
    #SELECT xd.Sigla, xs.Nombre, xs.Apellido, xd.nota1, xd.nota2, xd.notafinal FROM alumno_asignatura xd, alumno xs WHERE xd.Ci = xs.Ci;
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todas las asignaturas
    cursor = conn.execute('SELECT xd.Sigla, xs.Ci, xs.Nombre, xs.Apellido, xd.nota1, xd.nota2, xd.notafinal FROM alumno_asignatura xd, alumno xs WHERE xd.Ci = xs.Ci;')

    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>Sigla</th><th>Ci</th><th>Nombre</th><th>Apellido</th><th>Nota 1</th><th>Nota 2</th><th>Nota Final</th><th>Acciones</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td>'
        html += f'<td><a href="editar_notas?sigla={row[0]}&ci={row[1]}&nombre={row[2]}&apellido={row[3]}&nota1={row[4]}&nota2={row[5]}&notafinal={row[6]}" class="btn btn-success">Editar</a></td>  &ensp;'
        html += f'<td><a href="baja_estudiante?sigla={row[0]}&ci={row[1]}" class="btn btn-danger">Eliminar</a></td></tr>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html

def inscribir_estudiante(ci, sigla, nota1, nota2, notafinal):
    conn = sqlite3.connect('academico.db')

    conn.execute(f'INSERT INTO alumno_asignatura (Ci, Sigla, nota1, nota2, notafinal) VALUES ({ci}, "{sigla}", {nota1}, {nota2}, {notafinal});')

    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def baja_asignatura_estudiante(ci, sigla):
    conn = sqlite3.connect('academico.db')

    conn.execute(f'DELETE FROM alumno_asignatura WHERE Ci = {ci} AND Sigla LIKE "{sigla}";')

    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def actualizar_notas(ci, sigla, nota1, nota2, notafinal):
    conn = sqlite3.connect('academico.db')

    conn.execute(f'UPDATE alumno_asignatura SET nota1 = {nota1}, nota2 = {nota2}, notafinal = {notafinal} WHERE Sigla LIKE "{sigla}" AND Ci = {ci}')
    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def mostrar():
    # codigo para mostrar tabla alumno en pagina web
    html1 = select_alumnos()

    # codigo para mostrar tabla asignatura en pagina web
    html2 = select_asignatura()

    html3 = select_asignatura_estudiante()

    # Cargamos el archivo HTML
    with open('index.html', 'r') as file:
        html = file.read()

    # Reemplazar las variables en la cadena de formato
    html = html.format(html1=html1, html2=html2, html3=html3)
    return html

#ver asignaturas de un alumno
def alumno_asignatura(ci):
    #SELECT xd.Sigla, xs.Nombre, xs.Apellido, xd.nota1, xd.nota2, xd.notafinal FROM alumno_asignatura xd, alumno xs WHERE xd.Ci = xs.Ci;
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todas las asignaturas
    cursor = conn.execute("SELECT a.Sigla, a.Nombre, a.Semestre, aa.nota1, aa.nota2, aa.notafinal, aa.Ci FROM alumno_asignatura aa JOIN asignatura a ON aa.Sigla = a.Sigla WHERE aa.Ci = ?", (ci,))


    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>Sigla</th><th>Asignatura</th><th>Semestre</th><th>Nota 1</th><th>Nota 2</th><th>Nota Final</th><th>Acciones</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td>'
        html += f'<td><a href="baja_estudiante?sigla={row[0]}&ci={row[6]}" class="btn btn-danger">Eliminar</a></td></tr>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html

#ver alumnos de asignatura
def asignatura_alumno(sigla):
    #SELECT xd.Sigla, xs.Nombre, xs.Apellido, xd.nota1, xd.nota2, xd.notafinal FROM alumno_asignatura xd, alumno xs WHERE xd.Ci = xs.Ci;
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todas las asignaturas
    cursor = conn.execute("SELECT a.Ci, a.Nombre, a.Apellido, a.fecha_nac, aa.nota1, aa.nota2, aa.notafinal, aa.Sigla FROM alumno_asignatura aa JOIN alumno a ON aa.Ci = a.Ci WHERE aa.Sigla = ?", (sigla,))


    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>Ci</th><th>Nombre</th><th>Apellido</th><th>Fecha nacimiento</th><th>Nota 1</th><th>Nota 2</th><th>Nota Final</th><th>Acciones</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td>'
        html += f'<td><a href="baja_estudiante?sigla={row[7]}&ci={row[0]}" class="btn btn-danger">Eliminar</a></td></tr>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html

def nota_alumno(sigla, ci):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de las notas del alumno en una asignatura
    cursor = conn.execute("SELECT a.Ci, a.Nombre, a.Apellido, aa.nota1, aa.nota2, aa.notafinal, aa.Sigla FROM alumno_asignatura aa JOIN alumno a ON aa.Ci = a.Ci WHERE aa.Sigla = ? AND aa.Ci = ?", (sigla, ci))

    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>Ci</th><th>Nombre</th><th>Apellido</th><th>Nota 1</th><th>Nota 2</th><th>Nota Final</th><th>Materia sigla</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html


def main():
    # Creamos un objeto de socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuramos la dirección y el puerto del servidor
    server_address = ('localhost', 1234)

    # Enlazamos el socket al puerto y dirección del servidor
    server_socket.bind(server_address)

    # Empezamos a escuchar las solicitudes de los clientes
    server_socket.listen(1)

    print(f'Servidor escuchando en {server_address[0]}:{server_address[1]}')

    # Creamos la tabla de contactos
    create_table()

    while True:

        # Esperamos a que llegue una conexión
        client_socket, client_address = server_socket.accept()

        # Leemos la solicitud del cliente
        request = client_socket.recv(1024).decode('utf-8')

        # Imprimimos la solicitud del cliente
        print(f'Solicitud recibida desde {client_address[0]}:{client_address[1]}:')
        print(request)

        #cargamos otra pagina
        if request.startswith('GET /insertar_alumno.html'):
            # Cargamos el archivo HTML
            with open('insertar_alumno.html', 'r') as file:
                html = file.read()
            #response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            response += html
            #para index.
        elif request.startswith('GET /index.html'):
                html=mostrar()

        #eliminar alumno
        elif request.startswith('GET /eliminar_alumno'):
            # Obtener el CI del alumno
            url_parts = urlparse(request)
            query_params = parse_qs(url_parts.query)
            ci = query_params.get('ci', [''])[0].split(' ')

            eliminar_alumno(ci[0])
            html=mostrar()
        
            #editar alumno
        elif request.startswith('GET /editar_alumno'):
            # Obtener los parámetros del GET
            parametros = request.split(' ')[1]
            query_params = parse_qs(parametros.split('?')[1])
            ci = query_params.get('Ci', [''])[0]
            nomb = query_params.get('Nombre', [''])[0].strip()
            ape = query_params.get('Apellido', [''])[0].strip()
            fech = query_params.get('fecha_nac', [''])[0].strip()


            # Cargar el archivo HTML
            with open('editar_alumno.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(ci=ci, Nombre=nomb, Apellido=ape, Fecha_nac=fech)

            #editar alumno
        elif request.startswith('GET /editar_notas'):
            # Obtener los parámetros del GET
            parametros = request.split(' ')[1]
            query_params = parse_qs(parametros.split('?')[1])
            sigla = query_params.get('sigla', [''])[0]
            ci = query_params.get('ci', [''])[0].strip()
            nombre = query_params.get('nombre', [''])[0].strip()
            apellido = query_params.get('apellido', [''])[0].strip()
            nota1 = query_params.get('nota1', [''])[0].strip()
            nota2 = query_params.get('nota2', [''])[0].strip()
            notafinal = query_params.get('notafinal', [''])[0].strip()

            # Cargar el archivo HTML
            with open('editar_notas.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(ci=ci, nombre=nombre, apellido=apellido, nota1=nota1, nota2=nota2, notafinal=notafinal, sigla=sigla)

            #si da en editar_asignatura
        elif request.startswith('GET /editar_asignatura'):
            # Obtener los parámetros del GET
            parametros = request.split(' ')[1]
            query_params = parse_qs(parametros.split('?')[1])
            Sigla = query_params.get('Sigla', [''])[0]
            Nombre = ' '.join(unquote_plus(query_params.get('Nombre', [''])[0]).split())
            semestre = query_params.get('Semestre', [''])[0].strip()

            # Cargamos el archivo HTML
            with open('actualizar_asignatura.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(Sigla=Sigla, Nombre=Nombre, Semestre=semestre)
        #eliminar asignatura
        elif request.startswith('GET /eliminar_asignatura'):
            # Obtener los datos de la asignatura
            print("xd")

            url_parts = urlparse(request)
            query_params = parse_qs(url_parts.query)
            sigla = query_params.get('sigla', [''])[0].split(' ')
            print(sigla[0]+"/-*/*-//*-*-//*-/*-*-/*-/*-/*-/")

            eliminar_asignatura(sigla[0])
            
            html=mostrar()

        elif request.startswith('GET /baja_estudiante'):
            # Obtener los datos de la asignatura
            url_parts = urlparse(request)
            query_params = parse_qs(url_parts.query)
            sigla = query_params.get('sigla', [''])[0].split(' ')[0]
            ci = query_params.get('ci', [''])[0].split(' ')[0]
            
            #print(ci, sigla)

            baja_asignatura_estudiante(ci, sigla)
            
            html=mostrar()

        #insertar asignatura
        elif request.startswith('GET /insertar_asignatura.html'):
            # Cargamos el archivo HTML
            with open('insertar_asignatura.html', 'r') as file:
                html = file.read()
            # Creamos una respuesta HTTP para el cliente
            print("pasa")
            response += html
            #<a href="inscribir_estudiante?ci={ci}&nombre={row[1]}&apellido={row[2]}">Eliminar</a>
        elif request.startswith('GET /inscribir_estudiante'):
            parametros = request.split(' ')[1]
            query_params = parse_qs(parametros.split('?')[1])
            ci = query_params.get('ci', [''])[0]
            nombre = query_params.get('nombre', [''])[0]
            apellido = query_params.get('apellido', [''])[0].strip()
            
            # Cargamos el archivo HTML
            with open('inscribir_estudiante.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(ci=ci, nombre=nombre, apellido=apellido)

            print(ci, nombre, apellido)
        elif request.startswith('GET /alumno_asignatura.html'):
            #consultar asignaturas de alumno x
            # Cargamos el archivo HTML
            with open('alumno_asignatura.html', 'r') as file:
                html = file.read()

            html = html.format(tabla=select_asignatura_estudiante())
            # Creamos una respuesta HTTP para el cliente
            #print("pasa")
            response += html
        elif request.startswith('GET /asignatura_alumno.html'):
            #consultar alumnos de asignatura x
            # Cargamos el archivo HTML
            with open('asignatura_alumno.html', 'r') as file:
                html = file.read()
                html = html.format(tabla=select_asignatura_estudiante())
            # Creamos una respuesta HTTP para el cliente
            #print("pasa")
            response += html
        elif request.startswith('GET /nota_alumno.html'):
            #consultar alumnos de asignatura x
            # Cargamos el archivo HTML
            with open('nota_alumno.html', 'r') as file:
                html = file.read()
            html = html.format(tabla=select_asignatura_estudiante())
            # Creamos una respuesta HTTP para el cliente
            #print("pasa")
            response += html
        else:
            html=mostrar()

        if request.startswith('POST /insertar_alumno'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Ci = envio.split('&')[0].split('=')[1]
            nombre = envio.split('&')[1].split('=')[1]
            apellido = envio.split('&')[2].split('=')[1]
            fecha_nac = envio.split('&')[3].split('=')[1]


            # Insertamos el alumno en la base de datos
            insert_alumno(Ci,nombre, apellido, fecha_nac)

            html = mostrar()

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Alumno registrado correctamente.</p>'

        if request.startswith('POST /insertar_asignatura'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Sigla = envio.split('&')[0].split('=')[1]
            nombre = envio.split('&')[1].split('=')[1]
            Semestre = envio.split('&')[2].split('=')[1]

            nombre = nombre.replace("+", " ")
            # Insertamos el alumno en la base de datos
            insert_asignatura(Sigla, nombre, Semestre)

            html = mostrar()

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Asignatura registrada correctamente.</p>'

        if request.startswith('POST /inscribir_estudiante'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            ci = envio.split('&')[0].split('=')[1]
            nombre = envio.split('&')[1].split('=')[1]
            apellido = envio.split('&')[2].split('=')[1]
            sigla = envio.split('&')[3].split('=')[1]

            nombre = nombre.replace("+", " ")
            # Insertamos el alumno en la base de datos
            inscribir_estudiante(ci, sigla, 0, 0, 0)

            html = mostrar()

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Asignatura registrada correctamente.</p>'

        #editar
        if request.startswith('POST /editar_alumno'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Ci = envio.split('&')[0].split('=')[1]
            nombre = envio.split('&')[1].split('=')[1]
            apellido = envio.split('&')[2].split('=')[1]
            fecha_nac = envio.split('&')[3].split('=')[1]


            # Insertamos el alumno en la base de datos
            editar_alumno(Ci,nombre, apellido, fecha_nac)

            #actualiza
            html = mostrar()

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Alumno editado correctamente.</p>'

                #editar
        if request.startswith('POST /mod_notas'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            ci = envio.split('&')[0].split('=')[1]
            sigla = envio.split('&')[3].split('=')[1]
            nota1 = envio.split('&')[4].split('=')[1]
            nota2 = envio.split('&')[5].split('=')[1]
            notafinal = envio.split('&')[6].split('=')[1]

            
            print(ci, sigla, nota1, nota2, notafinal)

            # Modificamos las notas del estudiante con ci
            
            actualizar_notas(ci, sigla, nota1, nota2, notafinal)

            #actualiza
            html = mostrar()

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Notas modificadas</p>'


        if request.startswith('POST /editar_asignatura'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Sigla = envio.split('&')[0].split('=')[1]
            nombre = envio.split('&')[1].split('=')[1]
            Semestre = envio.split('&')[2].split('=')[1]

            nombre = nombre.replace("+", " ")
            # Insertamos el alumno en la base de datos
            actualizar_asignatura(Sigla, nombre, Semestre)

            #actualiza
            html = mostrar()

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Asignatura editado correctamente.</p>'

        #para mostrar asignaturas de un alumno x
        if request.startswith('POST /alumno_asignatura'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Ci = envio.split('&')[0].split('=')[1]

            # Realizamos la consulta
            tabla=alumno_asignatura(Ci)

            # Cargamos el archivo HTML
            with open('alumno_asignatura.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(tabla=tabla)

        #para alumnos de asignatura x
        if request.startswith('POST /asignatura_alumno'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Sigla = envio.split('&')[0].split('=')[1]

            # Realizamos la consulta
            tabla=asignatura_alumno(Sigla)

            # Cargamos el archivo HTML
            with open('asignatura_alumno.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(tabla=tabla)

        #para alumnos de asignatura x
        if request.startswith('POST /nota_alumno'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Sigla = envio.split('&')[0].split('=')[1]
            Ci = envio.split('&')[1].split('=')[1]

            # Realizamos la consulta
            tabla=nota_alumno(Sigla, Ci)

            # Cargamos el archivo HTML
            with open('nota_alumno.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html = html.format(tabla=tabla)

        # Creamos una respuesta HTTP para el cliente
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        response += html

        # Enviamos la respuesta al cliente
        client_socket.sendall(response.encode())

        # Cerramos la conexión con el cliente
        client_socket.close()

if __name__ == '__main__':
    main()
