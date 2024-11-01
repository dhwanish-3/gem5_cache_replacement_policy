import m5
from m5.objects import *
from m5.params import *
from m5.util import addToPath

# Set the path to gem5 configuration files
addToPath("configs/common")
addToPath("configs/example")

# Import the LRUReplacementPolicy
# from m5.objects import LRU2ReplacementPolicy

# Define the system
system = System()

# Set up the clock and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "3GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the memory
system.mem_mode = "timing"  # Out-of-Order CPU requires 'timing' mode
system.mem_ranges = [AddrRange("4GB")]

# CPU configuration (OoO CPU with specified parameters)
system.cpu = DerivO3CPU()
system.cpu.numROBEntries = 192
system.cpu.numIQEntries = 64

# create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()

# Branch Predictor configuration
system.cpu.branchPred = TAGE_SC_L_8KB()  # Tage SC-L branch predictor

# L1 Instruction Cache configuration
system.cpu.icache = Cache(
    size="32kB",
    assoc=4,
    tag_latency=3,
    data_latency=3,
    response_latency=3,
    mshrs=32,
    tgts_per_mshr=16,
)

# L1 Data Cache configuration
system.cpu.dcache = Cache(
    size="32kB",
    assoc=4,
    tag_latency=3,
    data_latency=3,
    response_latency=3,
    mshrs=32,
    tgts_per_mshr=16,
)

# Connecting L1 caches to the CPU
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

# L2 Cache (LLC) configuration
system.l2cache = Cache(
    size="256kB",
    assoc=16,
    tag_latency=9,
    data_latency=9,
    response_latency=9,
    mshrs=32,
    tgts_per_mshr=16,
    replacement_policy=LRU2RP(),
    prefetcher=BOPPrefetcher(),
)

system.l2bus = L2XBar()

# Connecting L2 cache to the L1 caches
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

# Setting up the memory controller
system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports
system.l2cache.cpu_side = system.l2bus.mem_side_ports

# For X86 only we make sure the interrupts care connect to memory.
# Note: these are directly connected to the memory bus and are not cached.
# For other ISA you should remove the following three lines.
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Memory configuration (DDR3 1600 MHz)
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()  # DDR3 with 1600 MHz
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Create system memory
system.system_port = system.membus.cpu_side_ports

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    # thispath,
    # "../../../",
    "/home/dhwanish/Documents/Benchmarks/benchspec/CPU2006/401.bzip2/exe/bzip2_base.gcc43-64bit",
)

system.workload = SEWorkload.init_compatible(binary)

# Set up the workload
process = Process()

# to be modified
process.cmd = [binary]  # Update 'input_file' with the actual input file path
system.cpu.workload = process
system.cpu.createThreads()


# Root configuration
root = Root(full_system=False, system=system)

# Instantiate and start the simulation
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
