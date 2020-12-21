"""

"""


def process(operations):
    acc = 0
    count = 0
    executed = set()
    n = len(operations)
    while count < n and count not in executed:
        executed.add(count)
        operation, value = operations[count]
        value = int(value)
        if operation == 'acc':
            acc += value
        elif operation == 'jmp':
            count += value - 1  # decrement to account for auto-increment
        count += 1
    return count == n and count not in executed, acc


def solve1(operations):
    _, acc = process(operations)
    return acc


"""
--- Part Two ---
After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions 
were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in 
the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never 
leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find 
another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions 
are visited in this order:
nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6

After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last 
instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, 
acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value 
of the accumulator after the program terminates?
"""
OPERATION_MAP = {"nop": "jmp", "jmp": "nop", "acc": "acc"}


def solve2(operations):
    for idx, (operation, value) in enumerate(operations):
        operations[idx][0] = OPERATION_MAP[operation]
        completed, acc = process(operations)
        if completed:
            return acc
        operations[idx][0] = operation
    return None


if __name__ == "__main__":
    with open('../data/day8.txt', 'r') as f:
        data = f.read().split('\n')
        data = [i.split() for i in data]
    print(solve1(data))
    print(solve2(data))
