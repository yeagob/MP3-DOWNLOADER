¡Claro! Aquí tienes la información de la aplicación Free MP3 Downloader formateada en Markdown.

🎶 Free MP3 Downloader
Una sencilla aplicación web construida con Flask que permite a los usuarios descargar audio MP3 buscando títulos de canciones o obteniendo listas de canciones de álbumes/artistas utilizando la API de MusicBrainz.

Características
Búsqueda y Descarga: Permite descargar canciones individuales o listas de canciones.

Obtención de Listas: Recupera listas de canciones de álbumes o todas las canciones de un artista (limitado a 100 temas únicos).

Organización Automática: Organiza los archivos descargados en carpetas para álbumes o artistas.

Temas: Alternancia de modo oscuro/claro.

Progreso: Barra de progreso para descargas múltiples.

Avisos: Incluye aviso legal y agradecimientos a los colaboradores.

💻 Uso e Instrucciones
Ejecutar la Aplicación
Después de la instalación, ejecuta python app.py en tu terminal.

Abre un navegador web y navega a http://127.0.0.1:5000/.

Obtener Listas de Canciones (Fetching Tracklists)
Introduce el nombre del artista (obligatorio para obtener todas las canciones, opcional para álbumes).

Introduce el nombre del álbum (opcional; si se deja vacío y se proporciona el artista, se obtendrán hasta 100 canciones del artista).

Haz clic en "Fetch Tracklist".

El área de texto se rellenará con títulos de canciones en el formato "Título - Artista". Si tiene éxito, un modal lo confirmará; edita la lista si es necesario.

Descargar MP3s
Introduce los títulos de las canciones en el área de texto (uno por línea) o utiliza la lista obtenida.

Haz clic en "Download MP3(s)".

Para descargas múltiples, una barra de progreso mostrará el estado.

Al finalizar, aparecerán los enlaces de descarga y los archivos se guardarán en la carpeta downloads (o una subcarpeta para álbumes/artistas). Un modal notificará cuando termine, con información sobre la ubicación del archivo.

Alternancia de Tema
Haz clic en el icono de sol/luna en la esquina superior derecha para cambiar entre los modos oscuro y claro.

Notas
Las descargas buscan la máxima calidad disponible (~320kbps equivalente, dependiendo de la fuente).

Utilízalo de forma responsable; respeta los derechos de autor y los términos de YouTube.

🛠️ Instalación y Ejecución
La aplicación requiere Python, Flask, yt-dlp, musicbrainzngs y FFmpeg.

Windows
Instalar Python:

Descarga e instala Python desde python.org.

Asegúrate de marcar "Add Python to PATH" durante la instalación.

Instalar Dependencias:

Abre el Símbolo del sistema.

Ejecuta:

Bash

pip install flask yt-dlp musicbrainzngs
Instalar FFmpeg:

Descárgalo de ffmpeg.org/download.html (p. ej., static build para Windows).

Extrae el archivo y añade la carpeta bin a la variable de entorno PATH de tu sistema:

Busca "Editar las variables de entorno del sistema" en el menú Inicio.

Haz clic en "Variables de entorno" > Editar "Path" en Variables del sistema > Añade la ruta a la carpeta bin de FFmpeg (p. ej., C:\ffmpeg\bin).

Verifica: Ejecuta ffmpeg -version en el Símbolo del sistema.

Ejecutar la App:

Guarda el código como app.py en una carpeta.

En el Símbolo del sistema, navega a la carpeta: cd ruta\a\la\carpeta.

Ejecuta:

Bash

python app.py
Accede en http://127.0.0.1:5000/.

Linux
Instalar Python:

La mayoría de las distribuciones ya lo tienen preinstalado. Verifica: python3 --version.

Si no, instala: sudo apt update && sudo apt install python3 python3-pip (Ubuntu/Debian) o el equivalente para tu distribución.

Instalar Dependencias:

Ejecuta:

Bash

pip install flask yt-dlp musicbrainzngs
Instalar FFmpeg:

Ejecuta: sudo apt install ffmpeg (Ubuntu/Debian) o el equivalente.

Verifica: ffmpeg -version.

Ejecutar la App:

Guarda el código como app.py.

En la terminal, navega a la carpeta: cd ruta/a/la/carpeta.

Ejecuta:

Bash

python3 app.py
Accede en http://127.0.0.1:5000/.

Mac
Instalar Python:

Descárgalo de python.org o usa Homebrew: brew install python.

Instalar Dependencias:

Ejecuta:

Bash

pip install flask yt-dlp musicbrainzngs
Instalar FFmpeg:

Usa Homebrew:

Bash

brew install ffmpeg
Verifica: ffmpeg -version.

Ejecutar la App:

Guarda el código como app.py.

En Terminal, navega a la carpeta: cd ruta/a/la/carpeta.

Ejecuta:

Bash

python app.py
Accede en http://127.0.0.1:5000/.

⚙️ Explicación Técnica
Esta aplicación es un servidor web basado en Flask que integra:

yt-dlp para la extracción de audio de YouTube.

MusicBrainz para la obtención de listas de canciones.

JavaScript del lado del cliente para las interacciones de la UI.

Funcionamiento Interno
Frontend (HTML/CSS/JS)
La UI se renderiza a través de una plantilla tipo Jinja en Flask.

JavaScript maneja el envío de formularios mediante AJAX, la consulta de progreso (polling), la alternancia de temas (almacenada en localStorage) y los modales para feedback.

CSS proporciona un diseño responsive con gradientes, sombras y colores específicos para cada modo.

Backend (Rutas de Flask)
/: Maneja GET para la página inicial y POST para la descarga de canciones. Utiliza hilos (threading) para descargas en segundo plano y evitar bloqueos.

/fetch_tracklist: Obtiene listas de canciones de MusicBrainz. Almacena la información en la sesión para la creación de subcarpetas.

/status/: Consulta el progreso de la descarga.

/download/path:filename: Sirve los archivos descargados.

Proceso de Descarga
yt-dlp extrae el audio como MP3, buscando la mejor calidad.

Los archivos se guardan en la carpeta downloads o en la subcarpeta artista/álbum.

El progreso se rastrea en un diccionario global y se actualiza en un hilo dedicado.

Dependencias
Dependencia	Función
Flask	Framework web.
yt-dlp	Descargador de YouTube.
musicbrainzngs	Cliente de la API de MusicBrainz.
FFmpeg	(Instalado Separadamente) Necesario para la conversión de audio.

Exportar a Hojas de cálculo
Seguridad y Notas Adicionales
Se ejecuta localmente; no requiere alojamiento externo.

Sanea los nombres de archivo para evitar problemas.

Maneja los errores con modales de feedback.

Para contribuciones o problemas, abre un pull request o una issue en GitHub.

By Santiago Game Lover
