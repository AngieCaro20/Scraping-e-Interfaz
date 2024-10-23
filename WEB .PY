import requests  # Importa la biblioteca requests para hacer solicitudes HTTP
from bs4 import BeautifulSoup  # Importa BeautifulSoup para analizar el HTML de las páginas web
import tkinter as tk  # Importa tkinter para crear la interfaz gráfica (ventana)
from tkinter import scrolledtext  # Importa el widget ScrolledText para mostrar grandes volúmenes de texto con barra de desplazamiento

# Función para ejecutar el scraping
def iniciar_scraping():
    url = entrada_url.get()  # Obtiene la URL ingresada por el usuario en el campo de entrada
    resultado_texto.delete(1.0, tk.END)  # Limpia el contenido anterior en la caja de texto (desde el inicio hasta el final)

    # Realiza una solicitud HTTP GET a la URL proporcionada
    respuesta = requests.get(url)
    
    # Verifica si la solicitud fue exitosa (código 200 significa éxito)
    if respuesta.status_code == 200:
        # Analiza el contenido HTML de la página utilizando BeautifulSoup
        soup = BeautifulSoup(respuesta.content, "html.parser")
        
        # Busca todos los elementos 'div' que contienen un atributo 'onclick' en la página
        maquinas = soup.find_all("div", onclick=True)
        
        autores = set()  # Crea un conjunto vacío para almacenar los nombres de los autores (evita duplicados)
        conteo_maquinas = 1  # Inicializa un contador para las máquinas encontradas

        # Itera sobre cada 'div' encontrado
        for maquina in maquinas:
            onclick_text = maquina["onclick"]  # Extrae el valor del atributo 'onclick' de cada 'div'
            autor = onclick_text.split("'")[7]  # Extrae el autor desde la posición específica en el texto dividido
            autores.add(autor)  # Añade el autor al conjunto (solo se guarda una vez cada autor)
            nombre_maquina = onclick_text.split("'")[1]  # Extrae el nombre de la máquina desde el texto dividido
            conteo_maquinas += 1  # Incrementa el contador de máquinas

        # Inserta los autores encontrados en la caja de texto de la interfaz
        resultado_texto.insert(tk.END, "Autores encontrados:\n")
        for autor in autores:  # Itera sobre cada autor en el conjunto de autores
            resultado_texto.insert(tk.END, f"{autor}\n")  # Muestra cada autor en la caja de texto

        # Inserta una cabecera para la lista de máquinas encontradas
        resultado_texto.insert(tk.END, "\nMáquinas encontradas:\n")
        
        # Itera nuevamente sobre las máquinas para mostrar sus detalles
        for maquina in maquinas:
            onclick_text = maquina["onclick"]  # Extrae el texto del atributo 'onclick'
            nombre = onclick_text.split("'")[1]  # Extrae el nombre de la máquina
            dificultad = onclick_text.split("'")[3]  # Extrae el nivel de dificultad de la máquina
            autor = onclick_text.split("'")[7]  # Extrae el autor de la máquina
            # Inserta el nombre de la máquina, dificultad y autor en la caja de texto
            resultado_texto.insert(tk.END, f"{nombre} --> {dificultad} --> {autor}\n")
    else:
        # Si la solicitud falla, muestra el código de error en la caja de texto
        resultado_texto.insert(tk.END, f"Hubo un error al hacer una petición: {respuesta.status_code}")

# Crear la ventana principal
ventana = tk.Tk()  # Inicializa la ventana principal de la aplicación
ventana.title("Programa Scraping")  # Establece el título de la ventana
ventana.configure(bg='#00BA6E')  # Configura el color de fondo de la ventana (verde claro)

# Etiqueta y entrada de la URL
etiqueta_url = tk.Label(ventana, text="Ingrese la URL:", fg='white', bg='#00BA6E', font=("Arial", 14))  # Crea una etiqueta con texto "Ingrese la URL", con fuente Arial y tamaño 14
etiqueta_url.pack(pady=5)  # Muestra la etiqueta en la ventana y añade un margen vertical de 5 píxeles

entrada_url = tk.Entry(ventana, width=50, font=("Arial", 14))  # Crea un campo de entrada de texto para la URL con ancho de 50 caracteres y fuente Arial 14
entrada_url.pack(pady=8)  # Muestra el campo de entrada en la ventana y añade un margen vertical de 8 píxeles

# Botón para iniciar el scraping
boton_iniciar = tk.Button(ventana, text="Iniciar", command=iniciar_scraping, bg='#002C29', fg='white', activebackground='lightblue', font=("Arial", 14))  
# Crea un botón con el texto "Iniciar", que llama a la función iniciar_scraping cuando se presiona, con colores personalizados (fondo verde oscuro, texto blanco), y fuente Arial tamaño 14
boton_iniciar.pack(pady=10)  # Muestra el botón y añade un margen vertical de 10 píxeles

# Caja de texto para mostrar el resultado
resultado_texto = scrolledtext.ScrolledText(ventana, width=60, height=20, font=("Arial", 14))  # Crea una caja de texto con barra de desplazamiento, de 60 caracteres de ancho y 20 de alto, con fuente Arial tamaño 14
resultado_texto.pack(pady=12)  # Muestra la caja de texto en la ventana y añade un margen vertical de 12 píxeles

# Ejecutar la ventana
ventana.mainloop()  # Inicia el bucle principal de la ventana, manteniéndola abierta y lista para interactuar
