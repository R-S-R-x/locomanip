from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import gymnasium as gym
import LeggedManip_Lab.tasks

print("LeggedManip_Lab tasks ok")

envs = [
    k for k in gym.registry.keys()
    if "PIPER" in k.upper() or "B2" in k.upper() or "GO2" in k.upper()
]

print("\n".join(envs))

simulation_app.close()
