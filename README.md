# Simple Interface Controller (Enable/Disable)

### Funciones:
Habilitar/Deshabilitar una interfaz de red


### Modo de uso:
```
$ python main.py eth0 0
eth0 is down!

$ python main.py eth1 1
eth1 is up!

$ python main.py %(DEFAULT_INTERFACE)s --restart
Restarting '%(DEFAULT_INTERFACE)s' ...
'%(DEFAULT_INTERFACE)s' is down!
'%(DEFAULT_INTERFACE)s' is up!
```
