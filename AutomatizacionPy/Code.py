"""
This Python script automates tasks on a webpage called "Netegia" which is used for generating invoices 
and their corresponding receipts. The automation process navigates through the webpage's HTML elements, 
extracting specific data and storing it in arrays. These arrays are then used to call and manage various 
functions available on the webpage itself.

The goal of this automation is to streamline repetitive tasks, such as invoice creation and receipt management, 
saving time and reducing the possibility of human errors. By combining HTML parsing and Python's robust 
programming capabilities, this script ensures that the required tasks are completed efficiently and accurately.

Key features of the automation include:  
1. Iterating through the webpage structure to locate and interact with specific elements.  
2. Extracting necessary information from the HTML and storing it for further use.  
3. Using the collected data to trigger webpage functions and complete the desired operations.  

This project demonstrates the use of Python for web automation, focusing on practicality, efficiency, and 
problem-solving skills. Arrays, functions, and HTML parsing tools are utilized to ensure seamless interaction 
with the Netegia webpage. The script is part of a broader effort to improve workflows and explore creative 
solutions through programming.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import random
from selenium.webdriver.chrome.options import Options


# Ruta al ChromeDriver
chrome_driver_path = "Path to Chromedriver.exe"  # Cambia esta ruta si está en otro lugar
# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")  # Ignorar errores de certificados
chrome_options.add_argument("--ignore-ssl-errors")          # Ignorar errores SSL

# Configurar el Service para Selenium 4.x
service = Service(chrome_driver_path)

# Inicializar el navegador con opciones y servicio
driver = webdriver.Chrome(service=service, options=chrome_options)
# Abrir la URL de login
login_url = "https://app.netegia.com.ar/LogIn"
driver.get(login_url)
# Esperar para que la página cargue
time.sleep(random.randint(4, 5))
# Localizar los campos de usuario y contraseña
usuario_field = driver.find_element(By.ID, "usuario")
clave_field = driver.find_element(By.ID, "clave")

# Ingresar las credenciales
usuario_field.send_keys("Email")  # Cambia esto con tu usuario
clave_field.send_keys("Password")  # Cambia esto con tu contraseña
clave_field.send_keys(Keys.RETURN)
time.sleep(random.randint(4, 5))

# Ingresa a la parte de facturacion
Pendientes_url = "https://app.netegia.com.ar/app/ListarPresupuestos?comboCondicionDeFechaEmision=&fechaDesdeEmision=&fechaHastaEmision=&accionFiltro=filtrar&orden_columna=&orden_direccion=&orden_simbolo=&estadoComprobante=1&codSucursal=&codPuntoDeVenta=&numeroDeComprobante=&numeroPedidoWeb=&jurisdiccion=&tipoIntegracion=&tipoDeComprobante=&botonFiltrar=&pagina=0"
driver.get(Pendientes_url)
time.sleep(random.randint(4, 5))

# Esperar a que cargue la tabla
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.tr-presupuestos'))
)

def obtener_n_enlace_atrib(n, str, clasee):
    resultados = []
    # Encuentra todas las filas con la clase 'tr-presupuestos'
    rows = driver.find_elements(By.CSS_SELECTOR, clasee)
    for row in rows:
        # Encuentra todos los enlaces en la fila
        enlaces = row.find_elements(By.TAG_NAME, 'a')
        print(f"Enlaces encontrados: {len(enlaces)}")
        
        if len(enlaces) >= 3:
            # Intentar obtener el texto visible usando textContent
            texto_enlace = enlaces[n-1].get_attribute(str).strip()
            print(f"Tercer enlace texto usando textContent: {texto_enlace}")  # Imprimir el texto del tercer enlace
            resultados.append(texto_enlace)  # Obtener el tercer enlace
    return resultados

def verificarTabla(driver):
    try:
        # Buscar la tabla
        tabla = driver.find_element(By.CSS_SELECTOR, "#tablaDatosPagoML tbody")
        
        if tabla:
            # Buscar la primera fila
            primera_fila = tabla.find_element(By.TAG_NAME, "tr")
            
            if primera_fila:
                # Buscar la tercera celda
                tercer_td = primera_fila.find_elements(By.TAG_NAME, "td")[2]
                
                if tercer_td:
                    # Obtener el texto de la tercera celda y verificar
                    texto_td = tercer_td.text.strip()
                    return 1 if texto_td == "Aprobado" else 0
        return 0  # Retornar 0 si no encuentra la tabla, fila o celda
    except Exception as e:
        print(f"Error: {e}")
        return 0
    
def procesarFilas(driver, estadoArray):
    try:
        # Buscar todas las filas con la clase 'tr-presupuestos'
        filas = driver.find_elements(By.CSS_SELECTOR, "tr.tr-presupuestos")

        if len(estadoArray) != len(filas):
            print("El número de elementos en estado_array no coincide con el número de filas.")
            return

        # Iterar sobre las filas y eliminar aquellas con estado 0
        for index, fila in enumerate(filas):
            if estadoArray[index] == 0:
                # Eliminar la fila si el estado es 0
                driver.execute_script("arguments[0].remove();", fila)

        print("Terminado!")

    except Exception as e:
        print(f"Error: {e}")

def ejecutarMain(driver):
    estadoArray = []
    resultados2 = obtener_n_enlace_atrib(3, 'textContent', 'tr.tr-presupuestos')
    
    for i in range(len(resultados2)):
        try:
            # Ejecutar el script para cargar la orden
            driver.execute_script("cargarOrdenMeli(arguments[0], arguments[1]);", resultados2[i], '2')
            time.sleep(random.randint(3, 4))
            
            # Verificar la tabla y guardar el estado
            estado = verificarTabla(driver)
            estadoArray.append(estado)
        
        except Exception:
            # En caso de error, agregar 0 al estadoArray
            estadoArray.append(0)
        
    time.sleep(random.randint(4, 5))
    
    # Intentar cerrar el modal
    try:
        boton_cerrar_modal = driver.find_element(By.CSS_SELECTOR, "button.cancelar")
        if boton_cerrar_modal:
            boton_cerrar_modal.click()
            print("Proceso completado: Modal cerrado.")
    except Exception:
        print("Botón de cerrar modal no encontrado o error al cerrar.")
    
    time.sleep(random.randint(4, 5))
    
    # Procesar las filas con el estadoArray
    procesarFilas(driver, estadoArray)
    print(estadoArray)


def Facturar(driver):
    resultados3 = obtener_n_enlace_atrib(1, 'href', 'tr.tr-presupuestos')
    i = 0
    for res in resultados3:
        try:
            i += 1
            driver.get(res)
            time.sleep(random.randint(4, 5))
            
            btn_facturar = driver.find_element(By.ID, "btnFacturar")
            btn_facturar.click()
            time.sleep(random.randint(4, 5))
            
            btn_emitir = driver.find_element(By.ID, "btnGuardarDocumento")
            btn_emitir.click()
            time.sleep(random.randint(4, 5))
            
            dropdown = driver.find_element(By.ID, "tipoPagoBanco-0")
            select = Select(dropdown)
            select.select_by_value("4767")
            time.sleep(random.randint(4, 5))
            
            boton = driver.find_element(By.ID, "botonTodoABanco-0")
            boton.click()
            time.sleep(random.randint(4, 5))
            
            boton = driver.find_element(By.ID, "btnGuardarAltaDocumento")
            boton.click()
            time.sleep(random.randint(4, 5))
        
        except Exception:
            # Si ocurre un error, vuelve directamente a Pendientes_url
            driver.get(Pendientes_url)
        
        finally:
            # Asegura que siempre regrese a Pendientes_url después del intento
            driver.get(Pendientes_url)
    return i

def Comprobantes(driver, num):
    rows2 = obtener_n_enlace_atrib(1, 'href', 'tr[role="row"]')
    for i in range(num):
        driver.get(rows2[i])
        time.sleep(random.randint(4, 5))
        boton_descargar = driver.find_element(By.XPATH, "//button[contains(text(), 'Descargar')]")
        boton_descargar.click()
        time.sleep(random.randint(4, 5))
        enlace_enviar_meli = driver.find_element(By.ID, "botonEnviarMeli")
        enlace_enviar_meli.click()
        time.sleep(random.randint(4, 5))
    
ejecutarMain(driver)
Num = Facturar(driver)
print(Num)
time.sleep(random.randint(4, 5))
driver.get("https://app.netegia.com.ar/app/ReporteDeComprobantes?comboCondicionDeFecha=&fechaDesde=&fechaHasta=&estadoComprobante=&tipoPago=&codSucursal=&codPuntoDeVenta=&tipoDeComprobante=&numeroDeComprobante=&numeroPedidoWeb=&jurisdiccion=&monedaNoEditableHidden=&moneda=&observacionFiltro=&conceptoFactura=&descDetalleComprobante=&accionFiltro=limpiar&orden_columna=&orden_direccion=&orden_simbolo=&documento=&pagina=0")
time.sleep(random.randint(4, 5))
Comprobantes(driver, Num)
driver.get("https://app.netegia.com.ar/app/Inicio")
print("Proceso TERMINADO")
time.sleep(100) 
