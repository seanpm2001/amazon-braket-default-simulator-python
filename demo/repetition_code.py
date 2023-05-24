from braket.ir.openqasm import Program

from braket.default_simulator import StateVectorSimulator

ghz_qasm = """
OPENQASM 3;

qubit[3] q;
qubit[2] f;
output uint[3] cq;
output uint[2] cf;

// Initial state
// x q[0]; // uncomment to start with state 1

// Encoding
cnot q[0], q[1];
cnot q[0], q[2];

// single Bit flip error
x q[1];

// Flag qubit 0
cnot q[0], f[0];
cnot q[2], f[0];

// Flag qubit 1
cnot q[1], f[1];
cnot q[2], f[1];

cf = measure f;

// Correct error based on error syndrome
if (cf==2){
  x q[0];
}
if (cf==1){
  x q[1];
}
if (cf==3){
  x q[2];
}

// measure q
cq = measure q;

"""


device = StateVectorSimulator()
program = Program(source=ghz_qasm)


num_shots = 100
result = device.run(program, shots=num_shots, mcm=True)

for i in range(num_shots):
    cf = result["cf"][i]
    print(f"error syndrome = {cf:02b}")
    cq = result["cq"][i]
    print(f"final sample   = {cq:03b}")

    print()
