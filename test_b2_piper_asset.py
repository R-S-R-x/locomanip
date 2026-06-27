import torch
import tensordict
import rsl_rl

from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

from isaaclab.sim import SimulationContext
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.assets import ArticulationCfg
from isaaclab.utils import configclass

from LeggedManip_Lab.assets.b2_piper.b2_piper_articulation_cfg import B2_PIPER_CFG


@configclass
class SceneCfg(InteractiveSceneCfg):
    robot: ArticulationCfg = B2_PIPER_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")


sim = SimulationContext()
scene = InteractiveScene(SceneCfg(num_envs=1, env_spacing=2.5))

sim.reset()
scene.update(dt=sim.get_physics_dt())

robot = scene["robot"]

print("ASSET LOADED")

print("\nJOINT NAMES:")
for i, name in enumerate(robot.data.joint_names):
    print(i, name)

print("\nBODY NAMES:")
for i, name in enumerate(robot.data.body_names):
    print(i, name)

simulation_app.close()