import socket
import sqlite3
from urllib.parse import parse_qs, urlparse
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
        html += f'<td><a href="editar_asignatura?sigla={row[0]}">Editar</a></td>'
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



def eliminar_asignatura(sigla):
     # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Eliminamos el registro correspondiente
    conn.execute(f'DELETE FROM asignatura WHERE ci={sigla}')

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
            # Creamos una respuesta HTTP para el cliente
            print("pasa")
            #response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            response += html
        else:
            #para index.
            if request.startswith('GET /index.html'):
                # codigo para mostrar tabla alumno en pagina web
                html1 = select_alumnos()

                # codigo para mostrar tabla asignatura en pagina web
                html2 = select_asignatura()

                # Cargamos el archivo HTML
                with open('index.html', 'r') as file:
                    html = file.read()

                # Reemplazar las variables en la cadena de formato
                html = html.format(html1=html1, html2=html2)

            else:
                #eliminar alumno
                if request.startswith('GET /eliminar_alumno'):
                    # Obtener el CI del alumno
                    url_parts = urlparse(request)
                    query_params = parse_qs(url_parts.query)
                    ci = query_params.get('ci', [''])[0].split(' ')

                    eliminar_alumno(ci[0])
                    # Código para mostrar tabla alumno en página web
                    html1 = select_alumnos()

                    # Código para mostrar tabla asignatura en página web
                    html2 = select_asignatura()

                    # Cargar el archivo HTML
                    with open('index.html', 'r') as file:
                        html = file.read()

                    # Reemplazar las variables en la cadena de formato
                    html = html.format(html1=html1, html2=html2)
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

        if request.startswith('POST'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            envio = request.split('\r\n')[-1]
            Ci = envio.split('&')[0].split('=')[1]
            nombre = envio.split('&')[1].split('=')[1]
            apellido = envio.split('&')[2].split('=')[1]
            fecha_nac = envio.split('&')[3].split('=')[1]


            # Insertamos el alumno en la base de datos
            insert_alumno(Ci,nombre, apellido, fecha_nac)

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Alumno enviado correctamente.</p>'

        # Creamos una respuesta HTTP para el cliente
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        response += html

        # Enviamos la respuesta al cliente
        client_socket.sendall(response.encode())

        # Cerramos la conexión con el cliente
        client_socket.close()

if __name__ == '__main__':
    main()