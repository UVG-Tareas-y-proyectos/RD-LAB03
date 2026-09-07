

<!-- Start of picture text -->
1966<br>Zze a4<br>=a<br>zE<br>5 =<br><!-- End of picture text -->

Excelencia que trasciende 



<!-- Start of picture text -->
a<br>Ko<br><!-- End of picture text -->

Nótese que Dijkstra y Flooding se usan en LSR, por lo que deben manejar alta <u>modularidad en sus</u> Clases y archivos. Además, sus programas deben ser capaces de correr Flooding y Dijkstra como el algoritmo de la red, independientemente de su uso en LSR (o sea, levantar los nodos en modo “flooding”, y enviarnos mensajes así, o levantarlo en modo Dijkstra y probarlo así aunque sepamos que es estático). 

## **3.2 Conexión y Pruebas de los algoritmos** 

La segunda parte del laboratorio consiste en conectar y probar nuestros algoritmos implementados. Usaremos como “red” nuestro servidor XMPP, por lo que cada nodo corresponde a un usuario/recurso en la red. 

<mark>Naturalmente, para poder probar y desarrollar sus algoritmos deberan conectarlos de alguna forma. Durante tal parte</mark> <u><mark>podrían utilizar sockets TCP temporalmente para agilizar el desarrollo de sus algoritmos</mark></u> <mark>(para poder probarlo todo localmente en sus computadoras, de forma offline, de ser necesario).</mark> 

Sin embargo, la conexión oficial de la segunda parte y la que se probara y entregarán DEBE hacerse via XMPP y el servidor que levantaremos la siguiente semana; el uso de sockets es temporal y para agilizar el desarrollo local, y poder enfocarse más en los algoritmos en la “primera parte”. 

Como toda Red, debemos definir protocolos y formatos estándares para comunicarnos. La base es la siguiente, pudiendo agregar elementos si así lo consideran ( **ojo, deben ponerse de acuerdo entre todos los grupos si modifican el protocolo. Esto significa que debería haber interoperabilidad entre codigos de distintos grupos en un mismo algoritmo** ). La estructura será tipo JSON y será de la siguiente forma: 

{ 

“proto” : ”dijkstra|flooding|lsr|dvr|...”, 

“type” : ”message|echo|info|hello|...”, 

“from” : ”foo@bar.com/123”, 

“to” : ”yolo@bar.com/777”, 

“ttl” : 5, 

“headers” : [{“opcional” : ”foo”}, {“alguna_optimizacion_suya” : ”bar”},  …], 

“payload” : “el contenido del paquete dependiendo de su tipo. Si es un mensaje de usuario seria algo como este texto y se debe forward a destino o print si somos nosotros destino. Si es un mensaje con info de tablas o enlace, aca iría ese contenido que cada nodo puede extraer del payload y utilizar para sus cálculos y tablas.” 

} 

## **3.3 Otros detalles para las pruebas y conexiones** 

El día de la entrega probaremos los algoritmos en clase. Para ello, se estará asignando una dirección/nombre a cada uno de los alumnos (nodos), quienes usarán su usuario “oficial” del servidor como ID y credenciales (mas detalle cuando entremos a esa fase la siguiente semana). Se estará brindando un archivo con la distribución de nombres (ver Anexo para tal formato). 

Los algoritmos a probar son <u>Flooding, Distance Vector y Link State Routing (Dijkstra y Flooding son</u> utilizados en LSR, Dijkstra no se probará directamente). 

Adicional, se establecerán mapas de conexiones entre nodos similar al de la Imagen 1. Se estará brindando un archivo con tal topología mencionada al momento de las pruebas (ver Anexo para el formato), la cual deben utilizar para configurar sus nodos y solamente para eso. Cualquiera de los nodos debe de tener la capacidad de enviar y/o recibir un mensaje. 

Al iniciar un nodo, este obtendrá la configuración y procederá a descubrir a sus vecinos. El nodo tendrá <u>dos procesos/hilos en simultáneo: el forwarding y el routing. Todo debe correr en paralelo/asíncrono</u> mediante el uso de hilos, procesos etc. Cada servicio se encarga de cosas específicas, como por ejemplo: 

- Forwarding 

   - Manejo de paquetes entrantes 

      - Paquetes de Datos: forward o print si es para nosotros 

      - Paquete de Info: dependiendo del algoritmo, como el Vector de Distancias o el LSP. Recibirlos y pasarlos al proceso de Ruteo. 

      - Paquete de Hello/Ping: Descubrimiento de nodos y medición de distancia hacia ellos. 

   - Manejo de paquetes salientes 

      - Forward messages 

      - Forward Flooding 

      - Forward DV/LSP/INFO 

      - Send Hello/Ping 

      - Confirmaciones de recepción, etc. 

- Routing 

   - Inicializar la Tabla de Ruteo 

   - Armar paquetes de Info 

   - Consultar paquetes de Info y nuevos nodos entrantes 

   - Utilizar paquetes de info para resolver y actualizar las tablas según cada algoritmo hace. 

Siguiendo el formato establecido, deberán <u>enviarse y definir distintos tipos de mensajes</u> para el funcionamiento de los algoritmos. Se sugiere un paquete tipo HELLO/PING, para medir delays entre nodos e inicializar nodos. Se sugiere un paquete _<u>DATA/MESSAGE</u>_ <u>, el cual contenga data de usuario</u> (mensajes) en su payload. Se sugiere un paquete _<u>TABLE/INFO</u>_ <u>, el cual contenga información de tablas,</u> ruteo, vecinos, etc.. Pueden agregar otros tipos si así desean y les sirve. 

El objetivo es lograr que los algoritmos se estabilicen y los mensajes pasen por los nodos que corresponden a la ruta óptima, así como el poder responder o adaptarse a nuevos nodos, nodos caídos, etc.. 

## **4 Rúbrica de evaluación** 

|**Elemento**||**Ponderación**||
|---|---|---|---|
|**Código**||**75%**||
||Documentación,<br>orden,<br>comentarios,<br>limpieza,<br>legibilidad/funcionalidad balanceada, etc..||5%|
||Implementación de los Algoritmos, de forma eficiente y<br>optimizada.||70%|
|**Reporte Esc**|**rito**|**25%**||
||Encabezado, Ortografía, Formato Adecuado, Descripción<br>de la Práctica||2.5%|
||Descripción de los Algoritmos Utilizados y su<br>Implementación||10%|
||Resultados||5%|
||Discusión||5%|
||Conclusiones + Comentarios + Referencias||2.5%|



** Una inasistencia injustificada anula la nota del laboratorio. 

## **<u>Entregar en Canvas</u>** : 

1. <u>Archivo .pdf con su reporte en grupo</u> 

2. <u>Codigo utilizado para el Laboratorio, en un rar si es necesario</u> 

3. <u>Link a su repositorio, el cual es privado hasta antes de la entrega</u> 

# **5  Anexo** 

El formato de los archivos de configuración será acorde al siguiente (se pondrán ejemplos en Canvas): 

- Topología de la Red: 

   - archivo: topo-*.txt 

   - contenido: JSON 

   - formato ejemplo: 

{“type”:”topo”, 

“config”: **{** “A”: [‘B’ , ’C’], “B”: [‘A’], …, ”D”: **[]** , ... **}** , } 

- Asignamiento de ID de Nodo: 

   - archivo: names-*.txt 

   - contenido: JSON 

   - formato ejemplo: 

{“type”:”names”, 

“config”: **{** “A”:”foo@bar.com”, “B”:”yolo@bar.com”,... **}** , 

} 

<u>NOTA IMPORTANTE: No está permitido usar los archivos de configuración para nada más</u> excepto el configurar su propio nodo y descubrir vecinos. A excepción de Dijkstra puro naturalmente y los procesos de Init() que usan esta información, no pueden usar eso para nada mas… por ejemplo, obtener toda la topología y resolver trivialmente de forma estática… en la realidad los routers tienen cables a sus vecinos pero desconocen el resto de la topología, y como pueden ver, los algoritmos a implementar todos son dinámicos. 

De igual manera, hacer eso resultará en errores, ya que le quita robustez al algoritmo (cambiamos algo del archivo de nombres, y corremos de nuevo y habrá problemas…). Es el equivalente a que se caiga un nodo, o que se conecte uno nuevo, o que al rato regrese el que se había caído. 

