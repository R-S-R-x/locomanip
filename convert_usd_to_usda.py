from pxr import Usd

src = r"C:\project\atec2\LeggedManip_Lab\source\LeggedManip_Lab\LeggedManip_Lab\assets\b2_piper\b2_piper.usd"
dst = r"C:\project\atec2\LeggedManip_Lab\source\LeggedManip_Lab\LeggedManip_Lab\assets\b2_piper\b2_piper_wrapper_text.usda"

stage = Usd.Stage.Open(src)
if stage is None:
    raise RuntimeError(f"Failed to open USD: {src}")

stage.Export(dst)
print("exported:", dst)