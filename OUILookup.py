import requests
import getopt
import sys
import os

# URL base de la API para consultar direcciones MAC
BASE_URL = "https://api.maclookup.app/v2/macs/"

# Función para obtener el fabricante a través de la MAC
def get_manufacturer(mac_address):
    try:
        response = requests.get(BASE_URL + mac_address)
        if response.status_code == 200:
            data = response.json()
            if 'company' in data:
                return data['company'], response.elapsed.total_seconds()
            else:
                return "Not found", response.elapsed.total_seconds()
        else:
            return "Error en la consulta", 0
    except Exception as e:
        return f"Error: {e}", 0

# Función para obtener las MACs de la tabla ARP (solo para sistemas Unix)
def get_arp_table():
    if os.name == "posix":
        arp_table = os.popen("arp -a").read()
        return arp_table
    else:
        return "Comando ARP solo disponible en sistemas Unix/Linux."

# Función para mostrar el mensaje de ayuda
def show_help():
    print("Use: OUILookup.py --mac <mac> | --arp | [--help]")
    print("--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
    print("--arp: muestra los fabricantes de los hosts disponibles en la tabla arp.")
    print("--help: muestra este mensaje y termina.")

# Función principal que maneja los argumentos
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hm:a", ["help", "mac=", "arp"])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    mac_address = None
    arp_flag = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-m", "--mac"):
            mac_address = arg
        elif opt == "--arp":
            arp_flag = True

    if mac_address:
        manufacturer, response_time = get_manufacturer(mac_address)
        print(f"MAC address : {mac_address}")
        print(f"Fabricante  : {manufacturer}")
        print(f"Tiempo de respuesta: {response_time * 1000:.2f} ms")
    elif arp_flag:
        arp_table = get_arp_table()
        print(f"Tabla ARP:\n{arp_table}")
    else:
        show_help()

if __name__ == "__main__":
    main(sys.argv[1:])
