from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import gymnasium as gym
import LeggedManip_Lab.tasks

envs = [k for k in gym.registry.keys() if "B2-PIPER" in k]
print(envs)

simulation_app.close()