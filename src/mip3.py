class CPU:
    def __init__(self):
        self.registers = [0] * 32
        self.registers[1:] = [1] * 31  # $0 is always 0, others default to 1
        self.memory = [1] * 32  # Memory initialized to 1
        self.pc = 0  # Program counter
        self.instructions = []  # Loaded instructions
        self.result_log = []  # Execution log
        self.cycles = 0

    def load_instructions(self, instructions):
        self.instructions = instructions

    def execute(self):
        while self.pc < len(self.instructions):
            self.run_pipeline()
            self.cycles += 1

    def run_pipeline(self):
        if self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            self.pc += 1
            self.run_instruction(instruction)

    def run_instruction(self, instruction):
        opcode = instruction["opcode"]
        operands = instruction["operands"]

        if opcode == "ADD":
            rd, rs, rt = self.parse_registers(operands)
            self.registers[rd] = self.registers[rs] + self.registers[rt]
        elif opcode == "SUB":
            rd, rs, rt = self.parse_registers(operands)
            self.registers[rd] = self.registers[rs] - self.registers[rt]
        elif opcode == "LW":
            rt, offset_base = operands[0], operands[1]
            offset, base = self.parse_memory_operand(offset_base)
            self.registers[self.parse_register(rt)] = self.memory[self.registers[base] + offset]
        elif opcode == "SW":
            rt, offset_base = operands[0], operands[1]
            offset, base = self.parse_memory_operand(offset_base)
            self.memory[self.registers[base] + offset] = self.registers[self.parse_register(rt)]
        elif opcode == "BEQ":
            rs, rt, offset = self.parse_registers_with_offset(operands)
            if self.registers[rs] == self.registers[rt]:
                self.pc += offset
        elif opcode == "JUMP":
            target = int(operands[0])
            self.pc = target

        self.log_stage(opcode, operands)

    def parse_registers(self, operands):
        return [int(op.replace(",", "")[1:]) for op in operands]

    def parse_registers_with_offset(self, operands):
        rs, rt, offset = [operand.replace(",", "") for operand in operands]
        return int(rs[1:]), int(rt[1:]), int(offset)

    def parse_register(self, reg):
        return int(reg.replace(",", "")[1:])

    def parse_memory_operand(self, operand):
        offset, base = operand.split('(')
        offset = int(offset)
        base = self.parse_register(base[:-1])
        return offset, base

    def log_stage(self, opcode, operands):
        self.result_log.append(f"Cycle {self.cycles}: {opcode} {' '.join(operands)}")

    def print_results(self):
        print("\nExecution Log:")
        print("\n".join(self.result_log))
        print("\nFinal Registers:")
        for i, value in enumerate(self.registers):
            print(f"${i}: {value}")
        print("\nFinal Memory:")
        print(self.memory[:32])

def parse_instruction(line):
    parts = line.split()
    opcode = parts[0].upper()
    operands = parts[1:] if len(parts) > 1 else []
    return {"opcode": opcode, "operands": operands}

if __name__ == "__main__":
    cpu = CPU()
    instructions = []

    print("請輸入 MIPS 指令（輸入空行結束）：")
    while True:
        line = input("> ").strip()
        if not line:
            break
        if line.startswith("#"):
            continue
        instructions.append(parse_instruction(line))

    cpu.load_instructions(instructions)
    cpu.execute()
    cpu.print_results()
