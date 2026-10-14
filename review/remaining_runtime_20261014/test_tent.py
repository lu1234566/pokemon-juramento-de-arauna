"""Prize transactions and normal-save retry; challenge entry is a fixture."""
import json
from runtime import *

boot()
fixture()
cases = []
for name, field, prefix in (("Verdanturf", 0xE6A, "VERDANTURF"), ("Fallarbor", 0xE6C, "FALLARBOR"), ("Slateport", 0xE6E, "SLATEPORT")):
    call("ClearBag")
    for item_id in list(range(1, constant("ITEMS_COUNT"))) * 3:
        if item_id != constant("ITEM_NEST_BALL") and call("GetItemPocket", item_id) == call("GetItemPocket", constant("ITEM_NEST_BALL")):
            call("AddBagItem", item_id, 99)
    assert not call("CheckBagHasSpace", constant("ITEM_NEST_BALL"), 1)
    write("gSpecialVar_0x8004", constant(prefix + "_TENT_FUNC_SET_PRIZE"), 2)
    write("gSpecialVar_0x8006", constant("ITEM_NEST_BALL"), 2)
    call("Call" + name + "TentFunction")
    sb2 = read("gSaveBlock2Ptr")
    assert read(sb2 + field, 2) == constant("ITEM_NEST_BALL")
    write("gSpecialVar_0x8004", constant(prefix + "_TENT_FUNC_GIVE_PRIZE"), 2)
    call("Call" + name + "TentFunction")
    assert read("gSpecialVar_Result", 2) == 0
    assert read(sb2 + field, 2) == constant("ITEM_NEST_BALL")
    assert quantity("ITEM_NEST_BALL") == 0
    save(Q / (name.lower() + "_pending.sav"))
    restore(Q / (name.lower() + "_pending.sav"))
    assert read(read("gSaveBlock2Ptr") + field, 2) == constant("ITEM_NEST_BALL")
    assert quantity("ITEM_NEST_BALL") == 0
    call("ClearBag")
    write("gSpecialVar_0x8004", constant(prefix + "_TENT_FUNC_GIVE_PRIZE"), 2)
    call("Call" + name + "TentFunction")
    assert read("gSpecialVar_Result", 2) == 1
    assert read(read("gSaveBlock2Ptr") + field, 2) == 0
    assert quantity("ITEM_NEST_BALL") == 1
    save(Q / (name.lower() + "_claimed.sav"))
    restore(Q / (name.lower() + "_claimed.sav"))
    assert quantity("ITEM_NEST_BALL") == 1
    assert read(read("gSaveBlock2Ptr") + field, 2) == 0
    snapshot(name.lower() + "_claimed_continue")
    cases.append({"tent": name, "full_bag_pending": True, "save_reload_pending": True, "retry_received_once": True, "save_reload_claimed": True, "scope": "native prize function; fixtures, not three challenge victories"})
    print(name, "prize transaction PASS", flush=True)

receipt = metadata() | {"cases": cases}
(Q / "tent_prize_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
