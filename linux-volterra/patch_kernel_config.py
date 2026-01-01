#!/usr/bin/env python3

import sys

inputfile = sys.argv[1]
outputfile = sys.argv[2]

# uncomment for testing
# inputfile = "/home/alex/src/git/x13s-alarm/linux-x13s/config"
# outputfile = "config.out"

with open(inputfile, "r") as f:
    lines = f.readlines()

anomalies = {
    "CONFIG_CC_IMPLICIT_FALLTHROUGH": '"-Wimplicit-fallthrough=5"',
}

x13s_options = {
    # Add support for my USB Wifi Card (Netgear Nighthawk A7500)
    "CONFIG_WLAN_VENDOR_MEDIATEK": "y",
    "CONFIG_MT76_CORE": "m",
    "CONFIG_MT76_LEDS": "y",
    "CONFIG_MT76_USB": "m",
    "CONFIG_MT76_CONNAC_LIB": "m",
    "CONFIG_MT792x_LIB": "m",
    "CONFIG_MT792x_USB": "m",
    "CONFIG_MT7921_COMMON": "m",
    "CONFIG_MT7921U": "m",
    "CONFIG_MT7601U": "n",
    "CONFIG_MT76x0U": "n",
    "CONFIG_MT76x0E": "n",
    "CONFIG_MT76x2E": "n",
    "CONFIG_MT76x2U": "n",
    "CONFIG_MT7603E": "n",
    "CONFIG_MT7615E": "n",
    "CONFIG_MT7663U": "n",
    "CONFIG_MT7663S": "n",
    "CONFIG_MT7915E": "n",
    "CONFIG_MT7921E": "n",
    "CONFIG_MT7921S": "n",
    "CONFIG_MT7996E": "n",
    "CONFIG_MT7925E": "n",
    "CONFIG_MT7925U": "n",
}
leftovers = []
for key in x13s_options:
    leftovers.append(key)

options = {}

new_lines = []
for line in lines:
    if line.startswith("#"):
        if "is not set" in line:
            foo = line.split("is not set")[0].strip()
            key = foo.split("#")[1].strip()
            new_lines.append((key, "not set"))
        else:
            new_lines.append(line)
    elif line == "\n":
        new_lines.append(line)
    else:
        key = line.split("=")[0]
        value = line.split("=")[1]
        new_lines.append((key, value))

output_lines = []
for line in new_lines:
    if isinstance(line, tuple):
        key, value = line
        if key in x13s_options:
            if value != x13s_options[key]:
                output_lines.append(f"{key}={x13s_options[key]}\n")
            else:
                output_lines.append(f"{key}={value}")
            leftovers.remove(key)
        elif key in anomalies:
            output_lines.append(f"{key}={anomalies[key]}\n")
        elif value != "not set":
            output_lines.append(f"{key}={value}")
        else:
            output_lines.append(f"# {key} is not set\n")
    else:
        output_lines.append(line)

for extra_config in leftovers:
    output_lines.append(f"{extra_config}={x13s_options[extra_config]}\n")

with open(outputfile, "w") as f:
    f.writelines(output_lines)

print("Done!")
print(leftovers)
