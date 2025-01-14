"""
Copyright [2022] Victor C Hall

Licensed under the GNU Affero General Public License;
You may not use this code except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/agpl-3.0.en.html

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import json
import logging

def patch_unet(ckpt_path, force_sd1attn: bool = False):
    """
    Patch the UNet to use updated attention heads for xformers support in FP32
    """
    unet_cfg_path = os.path.join(ckpt_path, "unet", "config.json")
    with open(unet_cfg_path, "r") as f:
        unet_cfg = json.load(f)


    if force_sd1attn:
        unet_cfg["attention_head_dim"] = [8, 8, 8, 8]
    else:     
        unet_cfg["attention_head_dim"] = [5, 10, 20, 20]

    logging.info(f" unet attention_head_dim: {unet_cfg['attention_head_dim']}")
    with open(unet_cfg_path, "w") as f:
        json.dump(unet_cfg, f, indent=2)
