import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_d_latch(dut):
    dut._log.info("Starting D latch test")

    # Tiny Tapeout required signals
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.rst_n.value = 1   # reset not used in your design

    d = dut.ui_in[0]
    e = dut.ui_in[1]
    q = dut.uo_out[0]

    # -----------------------------
    # 1️⃣ Enable HIGH → Q follows D
    # -----------------------------
    e.value = 1

    d.value = 0
    await Timer(1, units="ns")
    assert q.value == 0, "Q should follow D=0 when E=1"

    d.value = 1
    await Timer(1, units="ns")
    assert q.value == 1, "Q should follow D=1 when E=1"

    # -----------------------------
    # 2️⃣ Disable latch → Q holds
    # -----------------------------
    e.value = 0

    d.value = 0   # change D, but latch disabled
    await Timer(1, units="ns")
    assert q.value == 1, "Q should HOLD previous value when E=0"

    d.value = 1
    await Timer(1, units="ns")
    assert q.value == 1, "Q should still HOLD when E=0"

    # -----------------------------
    # 3️⃣ Re-enable → Q updates again
    # -----------------------------
    e.value = 1
    await Timer(1, units="ns")
    assert q.value == 1, "Q should update when E goes high"

    d.value = 0
    await Timer(1, units="ns")
    assert q.value == 0, "Q should follow D again when enabled"

    dut._log.info("D latch test PASSED")
