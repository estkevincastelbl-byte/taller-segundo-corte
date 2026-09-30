# Taller – Control de robots en PyBullet mediante ESP32

**Universidad Militar Nueva Granada – Ingeniería Mecatrónica**  
**Asignatura:** Micros y Laboratorio  
**Autor:** Kevin Philip Castelblanco Ramirez  
**Código:** 7004607

---

## Descripción

El taller integra una ESP32 como consola física con simulaciones robóticas ejecutadas en Python y PyBullet. Se desarrollan tres ejercicios: desplazamiento de un dron entre tres posiciones, control de un robot Baxter y control de un robot humanoide.

La ESP32 no ejecuta la física. Su función es leer pulsadores o joysticks y enviar órdenes por USB-Serial. El computador interpreta las órdenes y actualiza la simulación.

## Contenido

1. Arquitectura
2. Punto A – Dron A → B → C
3. Punto B – Baxter
4. Punto C – Robot humanoide
5. Materiales y software
6. Instalación
7. Explicación del código
8. Estructura del repositorio
9. Problemas comunes
10. Conclusiones
11. Referencias

---

## 1. Arquitectura

```mermaid
flowchart LR
    C["Consola física"] --> E["ESP32"]
    E -- "USB Serial 115200" --> P["Python"]
    P --> S["PyBullet"]
    S --> R["Robot simulado"]
```

Se mantiene separada la adquisición de entradas del cálculo físico. Esto permite cambiar la consola sin modificar el modelo de simulación.

---

## 2. Punto A – Dron A → B → C

### Objetivo

Mover un dron entre tres posiciones A, B y C, gestionando las órdenes desde la ESP32.

### Consola

Se utilizan tres pulsadores:

| Orden | GPIO |
|---|---:|
| A | 25 |
| B | 26 |
| C | 27 |

Los pulsadores se conectan entre el GPIO correspondiente y GND utilizando `INPUT_PULLUP`.

La ESP32 transmite:

```text
TARGET:A
TARGET:B
TARGET:C
```

### Posiciones de referencia

```python
A = [0.0, 0.0, 1.0]
B = [1.0, 0.8, 1.2]
C = [-0.8, 1.0, 1.0]
```

El script utiliza el controlador `DSLPIDControl` de `gym-pybullet-drones`. El controlador calcula las velocidades de los motores necesarias para llevar el cuadricóptero a la referencia seleccionada.

```mermaid
flowchart LR
 A["Botón A/B/C"] --> B["ESP32"]
 B --> C["TARGET:X"]
 C --> D["Python"]
 D --> E["DSLPIDControl"]
 E --> F["RPM motores"]
 F --> G["PyBullet"]
```

El repositorio moderno de `gym-pybullet-drones` incluye ejemplos PID de posición y velocidad, por lo que este ejercicio se estructura alrededor de esa interfaz.

---

## 3. Punto B – Baxter

### Objetivo

Desarrollar una consola con ESP32 para controlar de forma fluida diferentes articulaciones del robot Baxter.

### Consola

Se proponen dos joysticks analógicos:

| Señal | GPIO |
|---|---:|
| Joystick izquierdo X | 34 |
| Joystick izquierdo Y | 35 |
| Joystick derecho X | 32 |
| Joystick derecho Y | 33 |
| Abrir pinza | 25 |
| Cerrar pinza | 26 |

La ESP32 normaliza las entradas aproximadamente al intervalo `-1 a 1` y transmite:

```text
JOY,x1,y1,x2,y2,abrir,cerrar
```

Ejemplo:

```text
JOY,0.152,-0.603,0.024,0.818,0,0
```

Python carga el modelo Baxter y obtiene las articulaciones móviles directamente desde el URDF.

El movimiento utiliza:

```python
p.setJointMotorControl2(
    robot,
    joint,
    p.POSITION_CONTROL,
    targetPosition=objetivo
)
```

Esto permite que el joystick modifique progresivamente la referencia y produzca un movimiento continuo en vez de saltos entre posiciones.

### Modelo Baxter

El enunciado proporciona como referencia el repositorio `pybullet_robots` y el ejemplo `baxter_ik_demo.py`. El archivo del taller permite indicar la ubicación del URDF mediante:

```bash
python control_baxter.py --urdf RUTA_AL_BAXTER.urdf
```

De esta manera no se redistribuyen dentro de este repositorio archivos externos del modelo.

---

## 4. Punto C – Robot humanoide

### Objetivo

Crear una consola ESP32 para producir movimientos continuos en un robot humanoide.

La consola utiliza nuevamente dos joysticks:

```text
ESP32
  ↓
CTRL,x1,y1,x2,y2,b1,b2
  ↓
Python
  ↓
POSITION_CONTROL
  ↓
Humanoide PyBullet
```

El ejemplo utiliza `humanoid/humanoid.urdf`, incluido entre los datos de PyBullet.

Los cuatro ejes analógicos modifican cuatro referencias articulares. Se aplica una zona muerta para evitar que el ruido del joystick produzca movimiento cuando está centrado.

```python
if abs(valor) > 0.12:
    objetivo += valor * 0.01
```

---

## 5. Materiales y software

### Hardware

- ESP32.
- 3 pulsadores para el Punto A.
- 2 joysticks analógicos para los puntos B y C.
- 2 pulsadores adicionales.
- Protoboard.
- Cables jumper.
- Cable USB de datos.

### Software

- Python.
- PyBullet.
- PySerial.
- NumPy.
- `gym-pybullet-drones`.
- Arduino IDE o VS Code/PlatformIO.

---

## 6. Instalación

### Dependencias generales

```bash
pip install -r requirements.txt
```

### gym-pybullet-drones

Se recomienda instalar el proyecto desde su repositorio:

```bash
git clone https://github.com/learnsyslab/gym-pybullet-drones.git
cd gym-pybullet-drones
pip install -e .
```

### Punto A

Cargar:

```text
Punto_A_Drones/esp32/consola_drones.ino
```

Ejecutar:

```bash
python Punto_A_Drones/pc/control_drones.py --port COM5
```

### Punto B

Cargar:

```text
Punto_B_Baxter/esp32/consola_baxter.ino
```

Ejecutar indicando el modelo Baxter:

```bash
python Punto_B_Baxter/pc/control_baxter.py --port COM5 --urdf RUTA_AL_BAXTER.urdf
```

### Punto C

Cargar:

```text
Punto_C_Humanoide/esp32/consola_humanoide.ino
```

Ejecutar:

```bash
python Punto_C_Humanoide/pc/control_humanoide.py --port COM5
```

> Cambiar `COM5` por el puerto real de la ESP32.

---

## 7. Explicación del código

### ESP32

En los tres ejercicios la ESP32 funciona como interfaz de usuario. Los datos se envían a:

```cpp
Serial.begin(115200);
```

En el Punto A se detectan flancos de los pulsadores para no repetir continuamente una orden.

En Baxter y el humanoide se transmiten valores analógicos de manera periódica para obtener movimiento continuo.

### Python

PySerial recibe las líneas:

```python
serial.Serial("COM5", 115200)
```

Los comandos se transforman en referencias de posición para la simulación.

En los robots articulados se utiliza `POSITION_CONTROL`. En el dron se utiliza el controlador PID proporcionado por `gym-pybullet-drones`.

---

## 8. Estructura

```text
Taller/
├── README.md
├── requirements.txt
├── Punto_A_Drones/
│   ├── esp32/
│   │   └── consola_drones.ino
│   └── pc/
│       └── control_drones.py
├── Punto_B_Baxter/
│   ├── esp32/
│   │   └── consola_baxter.ino
│   └── pc/
│       └── control_baxter.py
└── Punto_C_Humanoide/
    ├── esp32/
    │   └── consola_humanoide.ino
    └── pc/
        └── control_humanoide.py
```

---

## 9. Problemas comunes

| Problema | Solución |
|---|---|
| Python no abre COM | Cerrar Monitor Serial y comprobar el puerto |
| Joystick se mueve solo | Aumentar la zona muerta |
| Baxter no carga | Indicar la ruta correcta con `--urdf` |
| No aparece el humanoide | Verificar instalación de `pybullet` |
| No se importa `gym_pybullet_drones` | Instalar el repositorio con `pip install -e .` |
| El dron es inestable | Verificar que la versión instalada sea compatible con el script |
| ESP32 no envía datos | Revisar baudrate 115200 y cable USB de datos |

---

## 10. Conclusiones

- La ESP32 puede utilizarse como consola física para controlar simulaciones robóticas ejecutadas en un computador.
- La separación entre consola y simulación simplifica la arquitectura y permite utilizar diferentes robots con una interfaz similar.
- En el dron, el control PID transforma una referencia de posición en acciones sobre los motores.
- En Baxter y el humanoide, los joysticks generan cambios graduales de referencia para obtener movimiento continuo.
- PyBullet permite integrar robots aéreos, manipuladores y humanoides dentro de un entorno común de simulación.

---

## 11. Referencias

- `gym-pybullet-drones`, proyecto de simulación y control de cuadricópteros en PyBullet.
- `pybullet_robots`, ejemplos de robots y Baxter.
- PyBullet Quickstart Guide.
- Espressif Systems – ESP32 Documentation.
- pySerial Documentation.

---

**Kevin Philip Castelblanco Ramirez**  
**Código: 7004607**
