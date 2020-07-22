import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.SP = 7
        self.reg[self.SP] = 0xF4
        self.pc = 0
        self.branchtable = {
            0b10000010: self.handle_LDI,
            0b01000111: self.handle_PRN,
            0b00000001: self.handle_HLT,
            0b10100010: self.handle_MUL,
            0b01000110: self.handle_POP,
            0b01000101: self.handle_PUSH,
        }


    def handle_POP(self, op_a, op_b):
        # "Pop the value at the top of the stack into the given register."
            # 1. Copy the value from the address pointed to by `SP` to the given register.
            # 2. Increment `SP`.

        # get register number for the binary code after pop instruction 
        reg_num = op_a
     
        key_in_stack = self.reg[self.SP]
        self.reg[reg_num] = self.ram[key_in_stack]

        self.reg[self.SP] += 1
        self.pc += 2

    def handle_PUSH(self, op_a, op_b):
        # decrement SP
        # F3
        self.reg[self.SP] -= 1   
       
        # get the value we want to store
        #  reg_num = self.ram[self.pc + 1] == 0000000 ??????
        # reg_num = op_a
        # value = self.reg[00000000] = 1
        # value = self.reg[reg_num]
        value = self.reg[op_a]
        # figure out where to store it
        # top_of_stack_addr = self.reg[self.SP] = F3
        # top_of_stack_addr = self.reg[self.SP]
        # store it
        # self.ram[top_of_stack_addr] = value | self.ram[f3] = 1
        # self.ram_write(value, top_of_stack_addr)
        self.ram_write(value, self.reg[self.SP])
        self.pc += 2

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