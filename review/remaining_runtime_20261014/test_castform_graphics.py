"""Compiled Tuim/Castform form sheets must fit every battle sprite slot.

This is an allocation/loading fixture, not evidence of campaign progression.
It reproduces the slot-3 heap overwrite without requiring a private save.
"""
from runtime import *

def memory(address, size):
    return bytes(read(address + i, 1) for i in range(size))

def heap_blocks():
    start, size = read('sHeapStart'), read('sHeapSize')
    address, blocks = start, []
    for _ in range(256):
        assert start <= address <= start + size - 16, hex(address)
        used, magic = read(address, 2), read(address + 2, 2)
        length, prev, nxt = [read(address + off) for off in (4, 8, 12)]
        assert used in (0, 1) and magic == 0xA3A3, ('invalid heap header', hex(address))
        assert address + 16 + length <= start + size
        assert start <= prev < start + size and start <= nxt < start + size
        blocks.append((address, length, used))
        if nxt == start:
            return blocks
        assert nxt > address and nxt == address + 16 + length
        assert read(nxt + 8) == address
        address = nxt
    raise AssertionError('heap block list did not terminate')

boot()
fixture()
call('AllocateMonSpritesGfx')
assert heap_blocks()
species = constant('SPECIES_CASTFORM')
front = SYMS['gMonFrontPicTable'] + species * 8
still = SYMS['gMonStillFrontPicTable'] + species * 8
front_length = read(read(front)) >> 8
back_length = read(read(SYMS['gMonBackPicTable'] + species * 8)) >> 8
assert front_length == 4 * 0x800, ('four form frames required', front_length)
assert back_length == 4 * 0x800
# Existing still-front sheet is the pixel reference; no replacement art.
reference = call('Alloc', front_length)
call('LZDecompressWram', read(still), reference)
expected = memory(reference, front_length)
gfx = read('gMonSpritesGfxPtr')
# struct MonSpritesGfx: firstDecompressed at +0, sprites.ptr[] at +4.
slots = [read(gfx + 4 + i * 4) for i in range(4)]
assert slots == [read(gfx) + i * 4 * 0x800 for i in range(4)]
checks = []
for slot, destination in enumerate(slots):
    call('HandleLoadSpecialPokePic_DontHandleDeoxys', front, destination, species, 0)
    assert memory(destination, front_length) == expected
    blocks = heap_blocks()
    # Exercise the allocator after the load, which hung with the bad sheet.
    allocation = call('AllocZeroed', 32)
    assert allocation
    call('Free', allocation)
    assert heap_blocks() == blocks
    checks.append({'slot': slot, 'four_form_frames_match_existing_art': True, 'heap_intact': True})
call('Free', reference)
call('FreeMonSpritesGfx')
assert heap_blocks()
(Q / 'castform_graphics_receipt.json').write_text(json.dumps(metadata() | {
    'test': 'native compiled sprite allocation/loading fixture',
    'front_bytes': front_length, 'back_bytes': back_length,
    'per_battler_capacity': 0x2000, 'slots': checks,
    'campaign_progression_claimed': False,
}, indent=2) + '\n')
print('Tuim/Castform four-form graphics, all battle slots and heap: PASS', flush=True)
