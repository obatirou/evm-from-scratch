#!/usr/bin/env python3

# EVM From Scratch
# Python template
#
# To work on EVM From Scratch in Python:
#
# - Install Python3: https://www.python.org/downloads/
# - Go to the `python` directory: `cd python`
# - Edit `evm.py` (this file!), see TODO below
# - Run `python3 evm.py` to run the tests

import json
import os

UINT256_MAX = 115792089237316195423570985008687907853269984665640564039457584007913129639935

def to_decimal(op):
    return int(op, 16)

def evm(code):
    pc = 0
    success = True
    stack = []

    while pc < len(code):
        op = code[pc]
        if op == to_decimal("00"):
            break
        if op == to_decimal("60"):
            pc += 1
            stack.append(code[pc])
        if op == to_decimal("61"):
            pc += 1
            stack.append(to_decimal(code[pc:pc+2].hex()) )
            pc += 2
        if op == to_decimal("63"):
            pc += 1
            stack.append(to_decimal(code[pc:pc+4].hex()) )
            pc += 4
        if op == to_decimal("65"):
            pc += 1
            stack.append(to_decimal(code[pc:pc+6].hex()) )
            pc += 6
        if op == to_decimal("69"):
            pc += 1
            stack.append(to_decimal(code[pc:pc+10].hex()) )
            pc += 10
        if op == to_decimal("6A"):
            pc += 1
            stack.append(to_decimal(code[pc:pc+11].hex()) )
            pc += 11
        if op == to_decimal("7F"):
            pc += 1
            stack.append(to_decimal(code[pc:pc+32].hex()) )
            pc += 31
        if op == to_decimal("50"):
            stack.pop()
        if op == to_decimal("01"):
            value = stack.pop() + stack.pop()
            if value > UINT256_MAX:
                value -= UINT256_MAX + 1
            stack.append(value)
        if op == to_decimal("02"):
            value = stack.pop() * stack.pop()
            if value > UINT256_MAX:
                value -= UINT256_MAX + 1
            stack.append(value)
        if op == to_decimal("03"):
            value = stack.pop() - stack.pop()
            if value < 0:
                value += UINT256_MAX + 1
            stack.append(value)
        if op == to_decimal("04"):
            a = stack.pop()
            b = stack.pop()
            if b == 0:
                value = 0
            else:
                value = a // b
            stack.append(value)
        if op == to_decimal("06"):
            a = stack.pop()
            b = stack.pop()
            if b == 0:
                value = 0
            else:
                value = a % b
            stack.append(value)
        if op == to_decimal("08"):
            a = stack.pop()
            b = stack.pop()
            c = stack.pop()
            value = a + b
            if value > UINT256_MAX:
                value -= UINT256_MAX + 1
            if c == 0:
                value = 0
            else:
                value %= c
            stack.append(value)
        pc += 1

    if stack:
        stack.reverse()
    return (success, stack)

def test():
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dirname, "..", "evm.json")
    with open(json_file) as f:
        data = json.load(f)
        total = len(data)

        for i, test in enumerate(data):
            # Note: as the test cases get more complex, you'll need to modify this
            # to pass down more arguments to the evm function
            code = bytes.fromhex(test['code']['bin'])
            (success, stack) = evm(code)

            expected_stack = [int(x, 16) for x in test['expect']['stack']]
            
            if stack != expected_stack or success != test['expect']['success']:
                print(f"❌ Test #{i + 1}/{total} {test['name']}")
                if stack != expected_stack:
                    print("Stack doesn't match")
                    print(" expected:", expected_stack)
                    print("   actual:", stack)
                else:
                    print("Success doesn't match")
                    print(" expected:", test['expect']['success'])
                    print("   actual:", success)
                print("")
                print("Test code:")
                print(test['code']['asm'])
                print("")
                print("Hint:", test['hint'])
                print("")
                print(f"Progress: {i}/{len(data)}")
                print("")
                break
            else:
                print(f"✓  Test #{i + 1}/{total} {test['name']}")

if __name__ == '__main__':
    test()
