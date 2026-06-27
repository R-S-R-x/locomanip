from pxr import Sdf

paths = [
    r"C:\project\atec2\LeggedManip_Lab\source\LeggedManip_Lab\LeggedManip_Lab\assets\b2_z1\b2_z1.usd",
    r"C:\project\atec2\LeggedManip_Lab\source\LeggedManip_Lab\LeggedManip_Lab\assets\b2_piper\b2_piper.usd",
    r"C:\project\atec2\LeggedManip_Lab\source\LeggedManip_Lab\LeggedManip_Lab\assets\b2_piper\b2_piper.usda",
]

for p in paths:
    print("\n" + "=" * 100)
    print(p)
    layer = Sdf.Layer.FindOrOpen(p)
    if layer is None:
        print("FAILED TO OPEN")
        continue

    print("identifier:", layer.identifier)
    print("defaultPrim:", layer.defaultPrim)
    print("subLayerPaths:", list(layer.subLayerPaths))

    print("rootPrims:")
    for prim in layer.rootPrims:
        print("  prim:", prim.name, "specifier:", prim.specifier, "type:", prim.typeName)
        print("    references:", prim.referenceList.prependedItems)
        print("    payloads:", prim.payloadList.prependedItems)
        print("    info keys:", prim.ListInfoKeys())