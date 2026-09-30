import argparse,time,serial,pybullet as p,pybullet_data,math
ap=argparse.ArgumentParser(); ap.add_argument("--port",default="COM5"); ap.add_argument("--sin-esp",action="store_true")
a=ap.parse_args(); ser=None if a.sin_esp else serial.Serial(a.port,115200,timeout=.03)
p.connect(p.GUI); p.setAdditionalSearchPath(pybullet_data.getDataPath()); p.setGravity(0,0,-9.81)
p.loadURDF("plane.urdf"); robot=p.loadURDF("humanoid/humanoid.urdf",[0,0,1.1],useFixedBase=False)
joints=[j for j in range(p.getNumJoints(robot)) if p.getJointInfo(robot,j)[2]==p.JOINT_REVOLUTE]
q=[0.0]*min(4,len(joints))
print("Humanoide listo. Joysticks controlan cuatro articulaciones.")
while True:
 vals=[0,0,0,0,0,0]
 if ser:
  s=ser.readline().decode(errors="ignore").strip()
  if s.startswith("CTRL,"):
   try: vals=list(map(float,s.split(",")[1:]))
   except: pass
 for k,j in enumerate(joints[:4]):
  if abs(vals[k])>.12: q[k]+=vals[k]*.01
  q[k]=max(-1.2,min(1.2,q[k]))
  p.setJointMotorControl2(robot,j,p.POSITION_CONTROL,q[k],force=60)
 p.stepSimulation(); time.sleep(1/240)
