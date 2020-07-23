import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.branchtable = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b01000110: self.POP,
            0b01000101: self.PUSH,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100000: self.ADD
        }

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
    
    def RET(self, op_a, op_b):        
        # get variable for stack pointer for readability
        sp = self.registers[7]
        # get return index by figuring out where the stack pointer actually is in RAM
        return_index = self.ram[sp]
        # make the program counter point to where the stack pointer is
        self.pc = return_index
        # increment the stack pointer, which is a way of saying pop whatever was at the top OFF
        self.registers[7] += 1

    def CALL(self, op_a, op_b):
        # get address/index for the next instruction AFTER call  **not the register***
        return_index = self.pc + 2
        #  decrement Stack Pointer, aka get the address for the top of the stack
        self.registers[7] -= 1
        # assign the value of the top of the stack to the return_index, 
        # which is a way of saying we push the next instruction to the top of the stack
        self.ram[self.registers[7]] = return_index
        # set the program counter to whatever's in the register following the CALL instruction
        self.pc = self.registers[op_a]

    def POP(self, op_a, op_b):
        # get the stack pointer for readability 
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
        # decrement the stack pointer
        self.registers[7] -= 1
        # find the index for the next instruction and assign it to reg_num
        reg_num = op_a
        # look for the register number at that index and assign it to a value
        value = self.registers[reg_num]
        # get the stack pointer for readability 
        sp = self.registers[7]
        # to the top of the stack, assign the value
        self.ram[sp] = value
        # increment the program counter to next instruction
        self.pc += 2

    def LDI(self, op_a, op_b):
        self.registers[op_a] = op_b
        self.pc +=3

    def PRN(self, op_a, op_b):
        print(self.registers[op_a])
        self.pc +=2

    def HLT(self, op_a, op_b):
        exit()
    
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MULT":
            self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def MUL(self, op_a, op_b):
        self.alu("MULT", op_a, op_b)
        self.pc +=3
        
    def ADD(self, op_a, op_b):
        self.alu("ADD", op_a, op_b)
        self.pc +=3

    def load(self):
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
                print(f"could not find instruction {bin(IR)}")
                self.trace()
                exit()
            
            self.branchtable[IR](op_a, op_b)