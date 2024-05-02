import struct
import math
import os
import keystone
from keystone import *

def make_hex(x, r):
    p = math.floor(math.log(x, 2))
    a = round(16*(p-2) + x / 2**(p-4))
    if a<0: a += 128
    a = 2*a + 1
    h = hex(a).lstrip('0x').rjust(2,'0').upper()
    hex_value = f'0{r}' + h[1] + '02' + h[0] + '1E' 
    print(hex_value)
    return hex_value

def float2hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()

def patch_blyt(filename, pane, operation, value):
    print(f"Scaling {pane} by {value}")
    offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78} 
    full_path = filename
    with open(full_path, 'rb') as f:
        content = f.read().hex()
    start_rootpane = content.index(b'RootPane'.hex())
    pane_hex = str(pane).encode('utf-8').hex()
    start_pane = content.index(pane_hex, start_rootpane)
    idx = start_pane + offset_dict[operation]
    content_new = content[:idx] + float2hex(value) + content[idx+8:]
    with open(full_path, 'wb') as f:
        f.write(bytes.fromhex(content_new))


def make_special(num):
    num = round(num, 15)
    packed = struct.pack('!f', num)
    full_hex = ''.join('{:02x}'.format(b) for b in packed)
    hex_1 = full_hex[:4]
    hex_2 = full_hex[4:]
    hex_01 = hex_1[:2]
    hex_02 = hex_1[2:]
    hex_03 = hex_2[:2]
    hex_04 = hex_2[2:]
    asm = f".BYTE 0x{hex_04}, 0x{hex_03}, 0x{hex_02}, 0x{hex_01}"
    return asm_to_hex(asm)

def asm_to_hex(asm_code):
    ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    encoding, count = ks.asm(asm_code)
    return ''.join('{:02x}'.format(x) for x in encoding)

def make_super(register, num):
    num = round(num, 15)
    packed = struct.pack('!f', num)
    full_hex = ''.join('{:02x}'.format(b) for b in packed)
    hex_1 = full_hex[:4]
    hex_2 = full_hex[4:]
    asm1 = f'movz {register}, #0x{hex_2}'
    asm2 = f'movk {register}, #0x{hex_1}, lsl #16'
    return asm_to_hex(asm1), asm_to_hex(asm2)

def make_super_r(register, num):
    num = round(num, 15)
    packed = struct.pack('!f', num)
    full_hex = ''.join('{:02x}'.format(b) for b in packed)
    hex_1 = full_hex[:4]
    hex_2 = full_hex[4:]
    asm1 = f'movz {register}, #0x{hex_2}'
    asm2 = f'movk {register}, #0x{hex_1}, lsl #16'
    return asm_to_hex(asm2), asm_to_hex(asm1)

def make_super_s(register, num):
    num = round(num, 15)
    packed = struct.pack('!f', num)
    full_hex = ''.join('{:02x}'.format(b) for b in packed)
    hex_1 = full_hex[:4]
    hex_2 = full_hex[4:]
    asm1 = f'movz {register}, #0x{hex_2}, lsl #32'
    asm2 = f'movk {register}, #0x{hex_1}, lsl #48'
    return asm_to_hex(asm1), asm_to_hex(asm2)