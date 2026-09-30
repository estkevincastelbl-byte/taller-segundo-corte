"""
Control interactivo de Baxter en PyBullet.
Necesita el paquete/modelo Baxter disponible localmente.
--urdf permite indicar la ruta al baxter.urdf.
"""
import argparse, time, os, math, serial, pybullet as p, pybullet_data
ap=argparse.ArgumentParser()
ap.add_argument("--port",default="COM5")
ap.add_argument("--urdf",default="baxter_common/baxter_description/urdf/toms_baxter.urdf")
ap.add_argument("--sin-esp",action="store_true")
args=ap.parse_args()
ser=None if args.sin_esp else serial.Serial(args.port,115200,timeout=.03)

p.connect(p.GUI); p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.81); p.loadURDF("plane.urdf")
if not os.path.exists(args.urdf):
    raise FileNotFoundError("No se encontro Baxter. Use --urdf RUTA_AL_BAXTER.urdf")
robot=p.loadURDF(args.urdf,[0,0,0],useFixedBase=True)

moviles=[]
for j in range(p.getNumJoints(robot)):
    info=p.getJointInfo(robot,j)
    if info[2] in (p.JOINT_REVOLUTE,p.JOINT_PRISMATIC):
        moviles.append((j,info[1].decode(),info[8],info[9]))
print("Articulaciones:",[(j,n) for j,n,_,_ in moviles])

# Selección genérica de cuatro articulaciones móviles; puede ajustarse al URDF exacto.
q=[0.0]*min(4,len(moviles))
print("Consola lista. Joysticks mueven las primeras 4 articulaciones del URDF.")
while True:
    vals=[0,0,0,0,0,0]
    if ser:
        s=ser.readline().decode(errors="ignore").strip()
        if s.startswith("JOY,"):
            try: vals=list(map(float,s.split(",")[1:]))
            except: pass
    for k in range(min(4,len(q))):
        if abs(vals[k])>.12: q[k]+=vals[k]*0.012
        j,n,lo,hi=moviles[k]
        if lo<hi: q[k]=max(lo,min(hi,q[k]))
        p.setJointMotorControl2(robot,j,p.POSITION_CONTROL,q[k],force=80)
    p.stepSimulation(); time.sleep(1/240)
