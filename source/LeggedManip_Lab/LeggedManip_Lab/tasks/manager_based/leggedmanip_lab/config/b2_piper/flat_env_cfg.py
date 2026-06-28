# Copyright (c) 2025-2026, Junjie Zhu.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from isaaclab.utils import configclass
from ...leggedmanip_lab_env_cfg import LeggedManipLabEnvCfg
from LeggedManip_Lab.assets.b2_piper.b2_piper_articulation_cfg import (
    B2_PIPER_CFG,
    B2PIPER_JOINT_NAMES,
)
from LeggedManip_Lab.tasks.manager_based.leggedmanip_lab.leggedmanip_lab_env_cfg import *


@configclass
class   (ObservationsCfg):
    @configclass
    class PolicyCfg(ObsGroup):
        base_lin_vel = ObsTerm(func=mdp.base_lin_vel, scale=2.0)
        base_ang_vel = ObsTerm(
            func=mdp.base_ang_vel,
            noise=Unoise(n_min=-0.2, n_max=0.2),
            scale=0.2,
        )
        velocity_commands = ObsTerm(
            func=mdp.generated_commands,
            params={"command_name": "base_velocity"},
        )
        projected_gravity = ObsTerm(
            func=mdp.projected_gravity,
            noise=Unoise(n_min=-0.05, n_max=0.05),
        )
        joint_pos = ObsTerm(
            func=mdp.joint_pos_rel,
            noise=Unoise(n_min=-0.01, n_max=0.01),
        )
        joint_vel = ObsTerm(
            func=mdp.joint_vel_rel,
            noise=Unoise(n_min=-1.5, n_max=1.5),
            scale=0.05,
        )
        actions = ObsTerm(func=mdp.last_action)
        target_pose_commands = ObsTerm(
            func=mdp.generated_commands,
            params={"command_name": "ee_pose"},
        )

        def __post_init__(self):
            self.enable_corruption = True
            self.concatenate_terms = True
            self.history_length = 3

    policy: PolicyCfg = PolicyCfg()


@configclass
class B2PiperFlatEnvCfg(LeggedManipLabEnvCfg):
    observations: B2PiperTaskBObservationsCfg = B2PiperTaskBObservationsCfg()

    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # scene
        self.scene.robot: ArticulationCfg = B2_PIPER_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot"
        )

        # observations


        # curriculum

        # commands
        self.commands.base_velocity.curriculum_enabled = True
        self.commands.ee_pose.curriculum_enabled = True
        self.commands.ee_pose.ranges.pos_x = (0.35, 0.45)
        self.commands.ee_pose.ranges.pos_y = (-0.08, 0.08)
        self.commands.ee_pose.ranges.pos_z = (0.0, 0.15)
        self.commands.ee_pose.limit_ranges.pos_x = (0.35, 0.85)
        self.commands.ee_pose.limit_ranges.pos_y = (-0.35, 0.35)
        self.commands.ee_pose.limit_ranges.pos_z = (-0.2, 0.5)
        self.commands.ee_pose.limit_ranges.roll = (-0.6, 0.6)
        self.commands.ee_pose.limit_ranges.pitch = (-0.6, 0.6)
        self.commands.ee_pose.limit_ranges.yaw = (-0.8, 0.8)

        # events
        self.events.push_robot = None

        # actions
        self.actions.joint_pos.joint_names = B2PIPER_JOINT_NAMES
        self.actions.joint_pos.scale = 0.5
        self.actions.joint_pos.clip = None
        self.actions.joint_pos.use_default_offset = True
        self.actions.joint_pos.preserve_order = True

        # rewards
        self.curriculum.pos_cmd_levels.params["success_ratio"] = 0.25
        self.rewards.end_effector_position_tracking_exp.weight = 6.0
        self.rewards.end_effector_position_tracking_exp.params["std"] = 0.45
        self.rewards.end_effector_orientation_tracking.weight = -2.0
        self.rewards.track_lin_vel_xy_exp.weight = 2.0
        self.rewards.track_ang_vel_z_exp.weight = 1.0
        self.rewards.action_rate_l2.weight = -0.02
        self.rewards.arm_deviation.weight = -0.02
        self.rewards.arm_deviation.params["asset_cfg"].joint_names = B2PIPER_JOINT_NAMES[12:18]
        self.rewards.track_base_height_exp.params["target_height"] = 0.48

        # terminals

        self.disable_zero_weight_rewards()


class B2PiperFlatEnvCfg_PLAY(B2PiperFlatEnvCfg):
    def __post_init__(self) -> None:
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing event

        self.commands.base_velocity.ranges = self.commands.base_velocity.limit_ranges
        self.commands.ee_pose.ranges = self.commands.ee_pose.limit_ranges
