import os
import sys
import subprocess
import functions
import struct
import math

from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes, ultrawide_camera, inverse_factor):
    visual_fixesa = visual_fixes[0]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    inverse_factor = float(inverse_factor)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(inverse_factor, 2)
    hex_value2 = make_hex(inverse_factor, 8)
    hex_value3 = make_hex(inverse_factor, 0)
    hex_value_special = make_special(ratio_value)
    version_variables = ["13.0.1", "13.0.2"]
    hex_8r = make_super_r('w8', ratio_value)
    hex_22 = make_super('w22', ratio_value)
    hex_9 = make_super('w9', ratio_value)
    hex_22s = make_super_s('x22', ratio_value)
    hex_8 = make_super('w8', ratio_value)
    hex_15 = make_super('w15', ratio_value)
    hex_x12 = make_super('x12', ratio_value)
    hex_21 = make_super('w21', ratio_value)
    for version_variable in version_variables:
        file_name = f"{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "13.0.1":
            nsobidid = "B9B166DF1DB90BAFFBD8027EB0DF14D6949D6A11"
            hex1 = "035547A8"
            hex2 = "04470c5c"
            hex3 = "035abfec"
            hex4 = "004ee20c"
            visual_fix = visual_fixesa
            if ultrawide_camera == False:
                patch_stuff = f'''004f08a0 {hex_8r[0]}
004f089c {hex_8r[1]}
004f098c {hex_22[0]}
004f0990 {hex_22[1]}
004fe3a0 {hex_8r[0]}
004fe39c {hex_8r[1]}
014e5cec {hex_9[0]}
014e5cf0 {hex_9[1]}
014e5e04 {hex_22s[0]}
014e5e08 {hex_22s[1]}
014e62c4 {hex_8[0]}
014e62c8 {hex_8[1]}
029f9acc {hex_15[0]}
029f9ad0 {hex_15[1]}
0147f0c0 {hex_8[0]}
0147f0c4 {hex_8[1]}
0354d2dc {hex_x12[0]}
0354d2e0 {hex_x12[1]}
0361bd78 {hex_8r[0]}
0361bd78 {hex_8r[1]}
04470c5c {hex_value_special}
005050cc {hex_8[0]}
005050d0 {hex_8[1]}
005145ac {hex_9[0]}
005145b0 {hex_9[1]}
031573d4 {hex_21[0]}
031573d8 {hex_21[1]}
0051463c {hex_9[0]}
00514640 {hex_9[1]}
01493070 {hex_8[0]}
01493074 {hex_8[1]}
'''

        elif version_variable == "13.0.2":
            nsobidid = "CBD5A9B56EA859BA11CA069B19B666101AE56F5A"
            hex1 = "03555428"
            hex2 = "04471C5C"
            hex3 = "035abfec"
            hex4 = "004ee20c"
            visual_fix = visual_fixesa
            if ultrawide_camera == False:
                patch_stuff = f'''004F08C0 {hex_8r[0]}
004F08C4 {hex_8r[1]}
004F09AC {hex_22[0]}
004F09B0 {hex_22[1]}
004FE3C0 {hex_8r[0]}
004FE3C4 {hex_8r[1]}
014E5EFC {hex_9[0]}
014E5F00 {hex_9[1]}
014E6014 {hex_22s[0]}
014E6018 {hex_22s[1]}
014E64D4 {hex_8[0]}
014E64D8 {hex_8[1]}
029FA74C {hex_15[0]}
029FA750 {hex_15[1]}
0147F0E0 {hex_8[0]}
0147F0E4 {hex_8[1]}
0354DF5C {hex_x12[0]}
0354DF60 {hex_x12[1]}
0361C9F8 {hex_8r[0]}
0361C9F8 {hex_8r[1]}
04471C5C {hex_value_special}
005050EC {hex_8[0]}
005050F0 {hex_8[1]}
005145CC {hex_9[0]}
005145D0 {hex_9[1]}
03158054 {hex_21[0]}
03158058 {hex_21[1]}
0051465C {hex_9[0]}
00514660 {hex_9[1]}
01493090 {hex_8[0]}
01493094 {hex_8[1]}'''

        if ultrawide_camera == True:
            patch_stuff = f'''{hex1} {hex_value}
{hex2} {hex_value_special}
{hex3} {hex_value2}
{hex4} {hex_value3}'''
            
        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{patch_stuff}
@disabled

{visual_fix}

// Generated using SSBU-AAR by Fayaz (github.com/fayaz12g/ssbu-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")

# .BYTE 0x8e, 0xe3, 0x18, 0x40

# original camera variant:
# movk w8, #0x4018, lsl #16
# movz w8, #0xe38e
# movz w22, #0xe38e
# movk w22, #0x4018, lsl #16
# movk w8, #0x4018, lsl #16
# movz w8, #0xe38e
# movz w9, #0xe38e
# movk w9, #0x4018, lsl #16
# movk x22, #0xe38e, lsl #32
# movk x22, #0x4018, lsl #48
# movz w8, #0xe38e
# movk w8, #0x4018, lsl #16
# movz w15, #0xe38e
# movk w15, #0x4018, lsl #16
# movz w8, #0xe38e
# movk w8, #0x4018, lsl #16
# movz x12, #0xe38e
# movk x12, #0x4018, lsl #16
# movk w8, #0x4018, lsl #16
# movz w8, #0xe38e
# .BYTE 0x8e, 0xe3, 0x18, 0x40
# movz w8, #0xe38e
# movk w8, #0x4018, lsl #16
# movz w9, #0xe38e
# movk w9, #0x4018, lsl #16
# movz w21, #0xe38e
# movk w21, #0x4018, lsl #16
# movz w9, #0xe38e
# movk w9, #0x4018, lsl #16
# movz w8, #0xe38e
# movk w8, #0x4018, lsl #16

# 8(r), 22, 8(r), 9, 22(s), 8, 15, 8, x12, 8(r), hex_value_special, 8, 9, 21, 9, 8

