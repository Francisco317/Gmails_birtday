
#IMPORTACION DE LAS PAQUETERIAS 
from email.message import EmailMessage
import ssl
import smtplib
import csv 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

#INFORMACION DEL EMISOR DEL CORREO
#SE REQUIERE ACTIVAR VERIFICACION DE 2 PASOS EN GMAIL PARA OBTENER CONTRASEÑA
email_emisor = "colaboradorgm1@gmail.com"
email_contrasena = "rlesbmmgbviufztt"

#ASUNTO DEL MENSAJE, SE CREA LA VARIABLE PARA DESPUÉS MANDARLA TRAER"
asunto = "Buenos días compañero"


#AQUI MANDAMOS A TRAER EL ARCHIVO CSV Y DE DONDE SALDRA LA INFORMACION
with open('Workers.txt', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #ESTE FOR HARA QUE VAYAMOS REGISTRO POR REGISTRO MANDANDO CORREOS DEPENDIENDO DE LA INFO DE LA PERSONA
    for row in csv_reader:

        #AQUI CREAMOS LA VARIABLE FECHA_NACIMIENTO PARA QUE EL MODULO DATETIME LEA LA COLUMNA DE EL ARCHIVO CSV Y LO TOME COMO VARIABLE DE FECHA
        fecha_nacimiento = datetime.datetime.strptime(row['Fecha de nacimiento'], '%Y-%m-%d')
        # AQUI COMPROBAMOS SI LA VARIABLE DE FECHA_NACIMIENTO COINCIDE CON LA FECHA DEL DÍA DE HOY
        if fecha_nacimiento.month == datetime.datetime.today().month and fecha_nacimiento.day == datetime.datetime.today().day:
            #AQUI AGREGAMOS UN PEQUEÑO PRINT DE LA PERSONA A LA QUE SE LE ENVIO EL MENSAJE
            mensaje = f"¡Feliz cumpleaños, {row['Nombre']}!"
            print(mensaje)                     
        
            #CONTENIDO DEL MENSAJE PARA ENVIAR UN HTML
            html = """
                        <html>
                        <head>
                            <title>Tarjeta de Felicitación</title>
                            <style>
                                .card {
                                    width: 300px;
                                    background-color: #595bbb;
                                    padding: 20px;
                                    border-radius: 10px;
                                    margin: 0 auto;
                                    text-align: center;
                                    font-family: Arial, sans-serif;
                                }
                                .title {
                                    font-size: 24px;
                                    font-weight: bold;
                                    margin-bottom: 10px;
                                }
                                .message {
                                    font-size: 18px;
                                    margin-bottom: 20px;
                                }
                                .sender {
                                    font-size: 16px;
                                    font-style: italic;
                                }
                            </style>
                            </head>
                            <body>
                                <div class="card">
                                    <div class="title">Feliz Cumpleaños</div>
                                    <div class="message">¡Esperamos que tengas un excelente día y que sigas disfrutando de la vida!</div>
                                    
                                </div>
                        </body>
                        </html>
                    """

            #AQUI CONVERTIMOS LA VARIABLE HTML QUE ESTA INICIALIZADA COMO TEXTO EN UN ARCHIVO DE HTML
            cuerpo = MIMEText(html, 'html')

            #INFORMACIÓN SOBRE EL DESTINATARIO Y QUE VA A IR EN EL ASUNTO Y CONTENIDO
            email_receptor = (f'{row["email"]}')
            em = EmailMessage()
            em["From"] = email_emisor
            em["To"] = email_receptor
            em["Subject"] = asunto
            em.attach(cuerpo)
            em.set_content(cuerpo)

            contexto = ssl.create_default_context()

            #AQUI CON SMTPLIB ES DONDE SE ENVIA EL CORREO CON LA INFORMACION ANTERIOR
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
                smtp.login(email_emisor, email_contrasena)

                smtp.sendmail(email_emisor, email_receptor, em.as_string())

                smtp.quit()
            #ESTE PRINT SOLAMENTE NOS DA UNA CONFIRMACION DE QUE SE ENVIO EXITOSAMENTE EL MENSAJE
            print("Se envio el correo con exito")
    
