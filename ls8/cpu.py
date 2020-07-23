import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        # self.SP = 7
        self.pc = 0
        self.branchtable = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b01000110: self.POP,
            0b01000101: self.PUSH,
        }


    def POP(self, op_a, op_b):
        # "Pop the value at the top of the stack into the given register."
            # 1. Copy the value from the address pointed to by `SP` to the given register.
            # 2. Increment `SP`.


        # get the stack pointer (where do we look?)
        sp = self.registers[7]

        # # get register number for the binary code after pop instruction, to put value in later
        reg_num = op_a

        # use stack pointer to get the value
        value = self.ram[sp]

        # put the value into the given register
        self.registers[reg_num] = value

        self.registers[7] += 1
        self.pc += 2

    def PUSH(self, op_a, op_b):
        # decrement SP
        # F3
        self.registers[7] -= 1

        reg_num = op_a

        value = self.registers[reg_num]
        sp = self.registers[7]

        self.ram[sp] = value
        
        self.pc += 2

    def LDI(self, op_a, op_b):
        self.registers[op_a] = op_b
        self.pc +=3

    def PRN(self, op_a, op_b):
        print(self.registers[op_a])
        self.pc +=2

    def HLT(self, op_a, op_b):
        exit()

    def MUL(self, op_a, op_b):
        self.registers[op_a] = self.registers[op_a] * self.registers[op_b]
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
            self.registers[reg_a] += self.registers[reg_b]
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
            print(" %02X" % self.registers[i], end='')

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