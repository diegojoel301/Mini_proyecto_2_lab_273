import socket
import sqlite3
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
        html += f'<td><a href="editar_alumno?ci={ci}">Editar</a><a href="eliminar_alumno?ci={ci}">Eliminar</a></td></tr>'
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
        html += f'<td><a href="editar_asignatura?sigla={row[0]}&nombre={row[1]}&semestre={row[2]}">Editar</a></td>'
        html += f'<td><a href="eliminar_asignatura?sigla={row[0]}">Eliminar</a></td></tr>'
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

def eliminar_alumno(id):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Eliminamos el registro correspondiente
    conn.execute(f"DELETE FROM alumno WHERE CI='{id}'")


    # Guardamos los cambios y cerramos la conexión
    conn.commit()
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

def eliminar_asignatura(sigla):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Eliminamos el registro correspondiente
    conn.execute(f'DELETE FROM asignatura WHERE Sigla LIKE "{sigla}"')

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

    redirect_asignaturas = False

    while True:

        # Esperamos a que llegue una conexión
        client_socket, client_address = server_socket.accept()

        # Leemos la solicitud del cliente
        request = client_socket.recv(1024).decode('utf-8')

        # Imprimimos la solicitud del cliente
        print(f'Solicitud recibida desde {client_address[0]}:{client_address[1]}:')
        print(request)

        #cargamos otra pagina
        if request.startswith('GET /crear_asignatura'):
            # Cargamos el archivo HTML
            with open('insertar_asignatura.html', 'r') as file:
                html = file.read()
            # Creamos una respuesta HTTP para el cliente
            print("pasa")
            #response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            response = html
        elif request.startswith('GET /editar_asignatura'):
            # Cargamos el archivo HTML
            #with open('actualizar_asignatura.html', 'r') as file:
            #    html = file.read()
            # Creamos una respuesta HTTP para el cliente
            #print("pasa")
            #response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            #response = html

            url_parts = urlparse(request)
            query_params = parse_qs(url_parts.query)
            sigla = query_params.get('sigla', [''])[0].split(' ')[0]
            nombre = unquote_plus(query_params.get('nombre', [''])[0].split(' ')[0])
            semestre = query_params.get('semestre', [''])[0].split(' ')[0]
            print(sigla, nombre, semestre)

            html = ""
            html += '<!DOCTYPE html>'
            html += '<html>'
            html += '<head>'
            html += '<meta charset="utf-8">'
            html += '<meta name="viewport" content="width=device-width, initial-scale=1">'
            html += '<title>Insertar Asignatura</title>'
            html += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">'
            html += '</head>'
            html += '<html>'
            html += '<body>'
            html += '<form method="post" action="actualizar_materia">'
            html += '<label for="sigla">Sigla:</label>'
            html += f'<input type="text" id="Sigla" name="sigla" value = "{sigla}" readonly><br>'
            html += '<label for="nombre">Nombre de Asignatura:</label>'
            html += f'<input type="text" id="nombre" name="nombre" value = "{nombre}" required><br>'
            html += '<label for="semestre">Semestre</label>'
            html += f'<input type="text" id="semestre" name="semestre" value = "{semestre}" required><br>'
            html += '<input type="submit" value="Enviar" class="btn btn-primary"><br>'
            html += '</form>'
            html += '<a href="/asignaturas" class="btn btn-success">Volver</a>'
            html += '</body>'
            html += '</html>'

            print(html)

            #para index.
        elif request.startswith('GET /asignaturas'):

            # codigo para mostrar tabla asignatura en pagina web
            html1 = select_asignatura()

            # Cargamos el archivo HTML
            with open('asignaturas.html', 'r') as file:
                html = file.read()

            # Reemplazar las variables en la cadena de formato
            html += html1

            html += '<a href="/crear_asignatura" class="btn btn-info" role="button">Crear Asignatura</a>'

            html += "</body></html>"

            print(html)


        #eliminar asignatura
        elif request.startswith('GET /eliminar_asignatura'):
            # Obtener los datos de la asignatura
            url_parts = urlparse(request)
            query_params = parse_qs(url_parts.query)
            sigla = query_params.get('sigla', [''])[0].split(' ')
            print(sigla)

            eliminar_asignatura(sigla[0])
            
            redirect_asignaturas = True

        else:
                # codigo para mostrar tabla alumno en pagina web
                html1 = select_alumnos()

                # codigo para mostrar tabla asignatura en pagina web
                html2 = select_asignatura()

                # Cargamos el archivo HTML
                with open('index.html', 'r') as file:
                    html = file.read()

                # Reemplazar las variables en la cadena de formato
                html = html.format(html1=html1, html2=html2)


        if request.startswith('POST /insertar_materia'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            sigla = envio.split('&')[0].split('=')[1]
            nombre_asignatura = unquote_plus(envio.split('&')[1].split('=')[1])
            semestre = envio.split('&')[2].split('=')[1]

            insert_asignatura(sigla, nombre_asignatura, semestre)

            redirect_asignaturas = True

        if request.startswith('POST /actualizar_materia'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            sigla = envio.split('&')[0].split('=')[1]
            nombre_asignatura = envio.split('&')[1].split('=')[1]
            semestre = envio.split('&')[2].split('=')[1]

            actualizar_asignatura(sigla, nombre_asignatura, semestre)

            redirect_asignaturas = True


        if not redirect_asignaturas:
            # Creamos una respuesta HTTP para el cliente
            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            
            response += html
            print(response)
        else:
            response = 'HTTP/1.1 301 Redireccion a Asignaturas\r\nLocation: /asignaturas\n\r\n\r'
            redirect_asignaturas = False

        # Enviamos la respuesta al cliente
        client_socket.sendall(response.encode())

        # Cerramos la conexión con el cliente
        client_socket.close()

if __name__ == '__main__':
    main()
