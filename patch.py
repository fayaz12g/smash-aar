import os
import sys
import subprocess
import functions
import struct
import math

from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):
    visual_fixesa = visual_fixes[0]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(ratio_value, 2)
    hex_value2 = make_hex(ratio_value, 8)
    hex_value3 = make_hex(ratio_value, 0)
    hex_value_special = make_special(ratio_value)
    version_variables = ["13.0.1", "13.0.2"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "13.0.1":
            nsobidid = "B9B166DF1DB90BAFFBD8027EB0DF14D6949D6A11"
            hex1 = "035547A8"
            hex2 = "04470c5c"
            hex3 = "035abfec"
            hex4 = "004ee20c"
            visual_fix = visual_fixesa

        elif version_variable == "13.0.2":
            nsobidid = "CBD5A9B56EA859BA11CA069B19B666101AE56F5A"
            hex1 = "03555428"
            hex2 = "04471C5C"
            hex3 = "035abfec"
            hex4 = "004ee20c"
            visual_fix = visual_fixesa

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{hex1} {hex_value}
{hex2} {hex_value_special}
{hex3} {hex_value2}
{hex4} {hex_value3}
@stop

{visual_fix}

// Generated using SSBU-AAR by Fayaz (github.com/fayaz12g/ssbu-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")

# .BYTE 0x8e, 0xe3, 0x18, 0x40