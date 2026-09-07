# Lab 3 - Algoritmos de Enrutamiento

## Estructura

```
src/
  main.py          punto de entrada (CLI)
  node.py          arma el nodo: hilo de forwarding + hilo de routing
  transport.py      sockets TCP, mandar/recibir paquetes en JSON
  packet.py         armar y leer el paquete del protocolo
  config.py         leer topo/names/addresses
  routing/
    base.py         interfaz comun de los algoritmos
    flooding.py
    dijkstra.py      calculo de caminos minimos + modo standalone
    lsr.py           link state (usa flooding.py y dijkstra.py)
    dvr.py           distance vector
config/              archivos de topologia/nombres/direcciones de ejemplo
tests/
  test_routing.py    pruebas rapidas de los algoritmos (sin frameworks)
```

## Como correr un nodo

Desde la raiz del repo:

```
python -m src.main <ID> --topo config/topo-example.txt \
    --addresses config/addresses-example.txt --algorithm <flooding|lsr|dvr|dijkstra>
```

Por ejemplo, para levantar los 5 nodos del topo de ejemplo con LSR (uno por
terminal):

```
python -m src.main A --topo config/topo-example.txt --addresses config/addresses-example.txt --algorithm lsr
python -m src.main B --topo config/topo-example.txt --addresses config/addresses-example.txt --algorithm lsr
python -m src.main C --topo config/topo-example.txt --addresses config/addresses-example.txt --algorithm lsr
python -m src.main D --topo config/topo-example.txt --addresses config/addresses-example.txt --algorithm lsr
python -m src.main E --topo config/topo-example.txt --addresses config/addresses-example.txt --algorithm lsr
```

Ya arriba, cada nodo tiene una consola simple:

```
send <destino> <mensaje>   manda un mensaje de usuario
table                      imprime la tabla de ruteo actual
quit                       cierra el nodo
```

Con `flooding` no hay tabla de ruteo, todo se manda por broadcast. Con `lsr`
y `dvr` hay que esperar unos segundos a que los nodos se pasen la info y
converjan antes de que `table` muestre algo util. Con `dijkstra` la tabla
sale de una vez porque lee la topologia completa (es la excepcion que
permite el enunciado, ya que ese modo no se usa para probar dinamismo).

## Configuracion

`topo-example.txt` y `names-example.txt` siguen el formato del anexo del
lab. `addresses-example.txt` es nuestro, mapea cada nodo a un `host:puerto`
local y solo sirve para las pruebas por socket, no es parte del protocolo
oficial.

## Protocolo

Cada paquete es un JSON con los campos `proto`, `type`, `from`, `to`, `ttl`,
`headers` y `payload`, tal como lo pide el enunciado. Ademas del `from`
(origen del mensaje), cada salto le agrega un header `hop` con el id de
quien lo esta reenviando, para que el vecino que lo recibe sepa por donde
le llego (sin eso no se puede excluir al vecino correcto al hacer
flooding).
