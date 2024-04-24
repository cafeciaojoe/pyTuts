"from the pybullet quickstart guide"
#https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit#heading=h.2ye70wns7io3

import pybullet as p
import time
import pybullet_data
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
startPos = [0,0,1]
startOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("r2d2.urdf",startPos, startOrientation)
boxId2 = p.loadURDF("cube.urdf",[0,1,.5], startOrientation)
#set the center of mass frame (loadURDF sets base link frame) startPos/Ornp.resetBasePositionAndOrientation(boxId, startPos, startOrientation)

for i in range (10000):
    #p.setJointMotorControlArray(bodyUniqueboxId, [2,3,2], 100)
    maxForce = 2
    # p.setJointMotorControl2(bodyUniqueId=boxId,
    #                         jointIndex=3,
    #                         controlMode=p.VELOCITY_CONTROL,
    #                         targetVelocity=100,
    #                         force=maxForce)
    p.setJointMotorControlArray(bodyIndex=boxId,
                            jointIndices=[2,3,6,7],
                            controlMode=p.VELOCITY_CONTROL,
                            targetVelocities=[-1000,-1000,-1000,-1000],
                            forces=[maxForce,maxForce,maxForce,maxForce])
    p.stepSimulation()
    p.rigi
    time.sleep(1./24000.)

cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)
print(boxId)
print(p.getNumJoints(boxId))
for i in range(0,15):
    print(p.getJointInfo(boxId,int(i)))
p.disconnect()
