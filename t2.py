def check_bracket(string):
    stack = []
    result = ""
    for index, c in enumerate(string):
        if c == '(':
            stack.append(index)
            result += " "
        elif c == ')':
            if len(stack) > 0:
                result += " "
                stack.pop()
            else:result += "?"
        else: result += " "
    while stack:
        pos = stack.pop()
        result = result[:pos] + "x" + result[pos+1:]
    return result

while True:
    input_string = input("请输入字符串，输入'q'退出")
    if (input_string == 'q') :break
    result = check_bracket(input_string)
    print(input_string)
    print(result)
