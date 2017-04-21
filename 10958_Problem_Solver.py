"""Attempt to solve 10,958 Problem using combinatorics and RPN."""
from itertools import product
# import signal
#
#
# def print_linenum(signum, frame):
#     print("Currently at line", frame.f_lineno)
#
#
# signal.signal(signal.SIGINT, print_linenum)

# [1, 2, '+', 3, '+', 4, '+', 5, '+', 6, 7, '+', 8, '^', '^', 9, '+']
# Gets caught up on it        gets caught on 15**(15**8) ^^^
# Maybe threading?


def main():
    operands = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    operators = product('+-*/', repeat=len(operands)-1)
    # operators = product('+-*/^|', repeat=len(operands)-1)
    # operators = product('+-', repeat=len(operands)-1)
    with open('results.txt', 'w') as f:
        for i, a in enumerate(operators):
            for g in gen_RPN(operands, a):
                # TODO Use eval_RPN on seperate thread and kill it if it takes
                # too long
                if eval_RPN(g) == 10958:
                    print(i, 'FOUND! ', g)
                    f.write(i, g)
            if i % 400 == 0:
                print(i)
    print('FINISHED')


def gen_RPN(operands, operators):
    """Generate RPN list based on operands and operators."""
    n = len(operators)-1
    for all_steps in steps(n, n):
        stack = list(operands[0:1])
        nr = 1
        for i, step in enumerate(all_steps):
            stack += operands[nr:nr+step]
            nr += step
            stack += operators[i]
        stack += operands[nr:]
        stack += operators[-1]
        yield stack


def eval_RPN(rpn):
    """Evaluate RPN equation."""
    stack = []
    operations = {
                '+': lambda x, y: y + x,
                '-': lambda x, y: y - x,
                '*': lambda x, y: y * x,
                '/': lambda x, y: y / x,
                '^': lambda x, y: y**x}
                # '|': lambda x, y: len(str(abs(int(x)))) * y + x}

    for a in rpn:
        if a in operations:
            try:
                stack.append(operations[a](stack.pop(), stack.pop()))
            except (ZeroDivisionError, OverflowError) as e:
                # print(e, ' on ', stack, ' when calculating ', rpn)
                return 0
        else:
            stack.append(a)
    try:
        return stack[0]
    except IndexError:
        print(rpn)
        quit()


def steps(n, total):
    """Yield n-sized list with sum of n."""
    if n == 1:
        yield (total,)
        return
    else:
        k = 0
        if total >= n:
            k = 1
        for i in range(k, total+1):
            for j in steps(n-1, total-i):
                yield (i,)+j


if __name__ == '__main__':
    main()
