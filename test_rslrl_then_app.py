import torch
print("torch", torch.__version__, torch.version.cuda)

import tensordict
print("tensordict", tensordict.__version__)

import rsl_rl
print("rsl_rl ok before app")

from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

print("app started after rsl_rl")

simulation_app.close()