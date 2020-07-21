import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branchtable = {
            0b10000010: self.handle_LDI,
            0b01000111: self.handle_PRN,
            0b00000001: self.handle_HLT,
            0b10100010: self.handle_MUL
        }

    def handle_LDI(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc +=3

    def handle_PRN(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc +=2

    def handle_HLT(self, op_a, op_b):
        exit()

    def handle_MUL(self, op_a, op_b):
        self.reg[op_a] = self.reg[op_a] * self.reg[op_b]
        self.pc +=3

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]
        with open(f"./examples/{filename}") as f:
            address = 0
            for line in f:
                line = line.split("#")
                try: 
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram[address] = v
                address +=1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)
            op_a, op_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)

            if IR not in self.branchtable:
                print(f"could not find instruction {IR}")
                self.trace()
                exit()
            
            self.branchtable[IR](op_a, op_b)