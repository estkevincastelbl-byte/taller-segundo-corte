"""
Control A/B/C para gym-pybullet-drones.
Requiere instalar el repositorio oficial/fork compatible y pyserial.
"""
import argparse, time, numpy as np, serial
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl

ap=argparse.ArgumentParser()
ap.add_argument("--port",default="COM5")
ap.add_argument("--sin-esp",action="store_true")
args=ap.parse_args()

PUNTOS={"A":np.array([0.0,0.0,1.0]),
        "B":np.array([1.0,0.8,1.2]),
        "C":np.array([-0.8,1.0,1.0])}

ser=None if args.sin_esp else serial.Serial(args.port,115200,timeout=.01)
env=CtrlAviary(drone_model=DroneModel.CF2X, num_drones=1,
               initial_xyzs=np.array([[0,0,0.1]]), physics=Physics.PYB,
               gui=True, ctrl_freq=48)
ctrl=DSLPIDControl(drone_model=DroneModel.CF2X)
target=PUNTOS["A"].copy()
obs,info=env.reset()

print("Listo. ESP32: botones A/B/C. Sin ESP32: escribe A, B o C y Enter.")
try:
  while True:
    if ser:
      line=ser.readline().decode(errors="ignore").strip()
      if line.startswith("TARGET:") and line[-1] in PUNTOS:
        target=PUNTOS[line[-1]].copy(); print("Destino",line[-1],target)
    state=obs[0]
    rpm,_,_=ctrl.computeControlFromState(control_timestep=env.CTRL_TIMESTEP,
                                         state=state,target_pos=target)
    obs,reward,terminated,truncated,info=env.step(np.array([rpm]))
    env.render()
    time.sleep(env.CTRL_TIMESTEP)
except KeyboardInterrupt:
  pass
finally:
  env.close()
  if ser: ser.close()
