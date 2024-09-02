from subprocess import run, PIPE
from argparse import ArgumentParser

DEFAULT_INTERFACE = "Ethernet"

def interface(name_of_interface:str, enabled:int|None):
    """
    Parámetros:
        - name_of_interface -- Nombre de la interfaz
        - enabled -- Habilitar (1) o deshabilitar (0) la interfaz
    """
    if enabled not in (1, 0, None):
        raise ValueError("values of parameter enabled must be either 1 or 0 integers or None")
    from platform import system as p_system
    p = p_system()
    if p == "Windows":
        if isinstance(enabled, int):
            cmd = "netsh interface set interface {} {}".format(name_of_interface, "admin=ENABLED" if enabled else "admin=DISABLED")
        else:
            cmd = "netsh interface show interface"
    elif p == "Linux":
        if isinstance(enabled, int):
            cmd = "ifconfig {} {}".format(name_of_interface, "up" if enabled else "down")
        else:
            cmd = "ifconfig -a"
    else:
        raise Exception("Unknown operating system!")

    filter_std = lambda x: x.decode("utf-8").strip() + "\r\n" if x else ""

    r = run(cmd, stdout=PIPE, stderr=PIPE)
    r.stdout = filter_std(r.stdout)

    if r.returncode == 0:
        if enabled in (1, 0):
            print("{} is {}\n".format(name_of_interface, "up!" if enabled else "down!"))
        else:
            print(r.stdout)
    else:
        r.stderr = filter_std(r.stderr)
        if r.stdout:
            print(r.stdout)
        if r.stderr:
            print(r.stderr)

    return r.returncode

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("enable_disable", type=int, nargs="?", default=None)
    parser.add_argument("-i", "--interface", type=str, nargs="?", default=DEFAULT_INTERFACE,
                        help="la interfaz a elegir: por defecto: ({})".format(DEFAULT_INTERFACE))
    args = parser.parse_args()

    if args.enable_disable != None and not isinstance(args.enable_disable, int) or isinstance(args.enable_disable, int) and args.enable_disable > 1:
        parser.error("argument enable_disable: must be 1 or 0")            

    exit(
        interface(
            name_of_interface=args.interface,
            enabled=args.enable_disable,
            )
        )
