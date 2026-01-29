@cocotb.test()
async def test_d_latch(dut):
    dut._log.info("Start D latch test")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    d = dut.ui_in[0]
    e = dut.ui_in[1]
    q = dut.uo_out[0]

    # Case 1: Enable = 1, D = 1 → Q should follow
    e.value = 1
    d.value = 1
    await Timer(1, units="us")
    assert q.value == 1, "Latch failed to pass D=1 when enabled"

    # Case 2: Enable = 1, D = 0 → Q should follow
    d.value = 0
    await Timer(1, units="us")
    assert q.value == 0, "Latch failed to pass D=0 when enabled"

    # Case 3: Disable latch, change D → Q should hold
    e.value = 0
    d.value = 1
    await Timer(1, units="us")
    assert q.value == 0, "Latch did not hold value when disabled"

    dut._log.info("D latch test PASSED")
