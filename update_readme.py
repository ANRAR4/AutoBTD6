from helper import *

fp = open("README.md")
oldREADME = fp.read()
fp.close()

output = re.sub(
    '<div id="map_parameter">.*?<\\/div>',
    '<div id="map_parameter">\n\n' + '\n'.join(map(lambda x: f'- `{x}`', maps.keys())) + '\n</div>',
    oldREADME,
    1,
    re.DOTALL,
)

output = re.sub(
    '<span id="version">.*?<\\/span>',
    f'<span id="version">{version}</span>',
    oldREADME,
    1,
    re.DOTALL,
)

if output == oldREADME:
    print("README identical after update")
else:
    fp = open("README.md", "w")
    fp.write(output)
    fp.close()

import generate_supported_maps_table