from Classes.mcu import MCU
import hardware as hrd
import re
import math
import numpy as np

line = 1
line_process = 0
def read_code(code_file_path):
    with open(code_file_path, 'r') as file:
        code = file.read()
    code = code.replace('(', ' ')
    code = code.replace(')', ' ')

    # Print the content
    delimiter_pattern = '|'.join(map(re.escape, [';', '\n', "'", '#', '^']))

    # Use re.findall to keep the delimiters
    words = re.findall(f'[^ {delimiter_pattern}]+|[{delimiter_pattern}]', code)
    return words



def create_array(sizes, value=0):
    # Base case: if sizes is empty, return the value
    if not sizes:
        return value
    # Recursive step: create a list of arrays of the remaining size
    return [create_array(sizes[1:], value) for _ in range(sizes[0])]


def get_element_array(element_list, array):
    # Base case: if sizes is empty, return the value
    if not element_list:
        return array
    # Recursive step: create a list of arrays of the remaining size
    return get_element_array(element_list[1:], array[element_list[0]])


def change_element_array(element_list, array):
    # Base case: if sizes is empty, return the value
    if not element_list:
        return array
    # Recursive step: create a list of arrays of the remaining size
    else:
        get_element_array(element_list[1:], array[element_list[0]])

line_error_list = []


def call_error(error_string):
    line_process = 0
    for l in line_error_list:
        if line == l:
            return
    print('[', line, ']:', error_string)
    line_error_list.append(line)


def debug(code_file):
    global line_process, line
    print("debugging...")
    words = read_code(code_file)
    memory = {}
    variables = []
    matrix_operations = {'*', '.*', "'", '^'}
    loop_condition = True
    idx = 0
    while loop_condition:
        loop_condition = idx < len(words)-1
        word = words[idx]
        if word == '\n':
            line = line + 1
            if line_process == 0:
                call_error("Line error")
            else:
                line_process = 0
        if word == '#':
            while words[idx] != '\n':
                idx = idx + 1
            line = line + 1
        elif word == 'assign':
            line_process = 1
            if words[idx + 2] == '=':
                variable = words[idx + 1]
                if variable.isalnum() and not variable.isnumeric():
                    operand = words[idx + 3]
                    cond = False
                    if operand.isnumeric():
                        variables.append(variable)
                        memory.update({variable: float(operand)})  # variable is not present and input is value
                    elif operand.isalnum():
                        for var in variables:
                            if operand == var:
                                cond = True
                        if cond:
                            cond2 = False
                            for var in variables:
                                if variable == var:
                                    cond2 = True
                            if cond2:
                                memory[variable] = memory(operand)  # variable and operand both are present in memory
                            else:
                                variables.append(variable)
                                memory.update({variable: memory(operand)})  # variable is not present but operand is present in memory
                        else:
                            error = "Variable not found: " + str(operand)
                            call_error(error)
                    else:
                        cond = False
                        var = operand.replace('[', ' ')
                        var = var.replace(']', ' ')
                        array_size = var.split()
                        operand = array_size.pop(0)
                        array_size = [int(size) for size in array_size]
                        if operand.isalnum() and not operand.isnumeric():
                            for var in variables:
                                if operand == var:
                                    cond = True
                            if cond:
                                try:
                                    memory.update({variable: get_element_array(array_size, memory[operand])})  # array element to variable
                                except IndexError:
                                    call_error("Index out of bound")
                                except TypeError:
                                    call_error("Accessing Float as Array")
                        else:
                            error = "Invalid Variable Access: " + str(operand)
                            call_error(error)
                else:  # array operations
                    cond = False
                    variable = variable.replace('[', ' ')
                    variable = variable.replace(']', ' ')
                    array_size = variable.split()
                    variable = array_size.pop(0)
                    if variable.isalnum() and not variable.isnumeric():
                        for var in variables:
                            if variable == var:
                                cond = True
                        if cond:
                            cond = False
                            element_pos = [int(size) for size in array_size]
                            flat_pos = math.prod(element_pos)
                            dimension = np.array(memory[variable]).shape
                            array = np.array(memory[variable]).flatten()
                            operand = words[idx+3]
                            if operand.isnumeric():
                                array[flat_pos] = float(operand)
                                array = array.reshape(dimension).tolist()
                                memory[variable] = array  # array element updation
                            elif operand.isalnum():
                                for var in variables:
                                    if operand == var:
                                        cond = True
                                if cond:
                                    cond2 = False
                                    for var in variables:
                                        if variable == var:
                                            cond2 = True
                                    if cond2:
                                        array[flat_pos] = memory[operand]
                                        array = array.reshape(dimension).tolist()
                                        memory[variable] = array
                                else:
                                    error = "Variable not found: " + str(operand)
                                    call_error(error)
                        else:
                            array_size = [int(size) for size in array_size]
                            flatten_size = math.prod(array_size)
                            array = np.zeros(flatten_size)
                            idx = idx + 2
                            for i in range(flatten_size):
                                idx = idx + 1
                                val = words[idx]
                                val = val.replace(',', '').replace('[', '').replace(']', '')
                                if val.isnumeric():
                                    array[i] = int(val)
                                else:
                                    call_error("Array size doesn't match")
                            idx = idx + 1
                            val = words[idx]
                            val = val.replace(',', '').replace('[', '').replace(']', '')
                            if val.isnumeric():
                                array[i] = int(val)
                                call_error("Array size doesn't match")
                            idx = idx - 1
                            array = array.reshape(array_size).tolist()
                            memory.update({variable: array})  # array instantiation
                            variables.append(variable)
                    else:
                        call_error("Invalid variable declaration")
            elif words[idx + 2] == ';':
                variable = words[idx + 1]
                variable = variable.replace('[', ' ')
                variable = variable.replace(']', ' ')
                array_size = variable.split()
                variable = array_size.pop(0)
                array_size = [int(size) for size in array_size]
                if variable.isalnum() and not variable.isnumeric():
                    array = np.zeros(array_size).tolist()
                    if variable in variables:
                        memory[variable] = array
                    else:
                        memory.update({variable: array})
                        variables.append(variable)
                else:
                    call_error("Invalid variable declaration")
            else:
                call_error("Incorrect use of Declare Statement")
        elif word == "sensor_read":
            line_process = 1
            sensor_id = words[idx + 1]
            variable = words[idx - 2]
            variables.append(variable)
            sensor_ = []
            for sensor in hrd.sensors_list:
                if sensor.id == sensor_id:
                    sensor_ = sensor
            if not sensor_:
                call_error("Invalid SENSOR Id Used in line")
            else:
                memory.update({variable: sensor_.read_sensor()})
        elif word == '+':
            line_process = 1
            variable = words[idx - 3]
            variables.append(variable)
            operand1 = words[idx - 1]
            operand2 = words[idx + 1]
            if operand1.isalpha() and operand2.isalpha():
                cond1, cond2 = False, False
                for var in variables:
                    if operand1 == var:
                        cond1 = True
                    if operand2 == var:
                        cond2 = True
                if cond2 and cond1:
                    memory.update({variable: memory[operand1] + memory[operand2]})
                else:
                    if cond1:
                        var = operand2
                    else:
                        var = operand1
                    error = "Variable not declared: " + str(var)
                    call_error(error)
            elif operand1.isnumeric() and operand2.isalpha():
                cond1 = operand2 in (operand2 for var in variables)
                operand1 = float(operand1)
                if cond1:
                    memory.update({variable: operand1 + memory[operand2]})
            elif operand2.isnumeric() and operand1.isalpha():
                cond1 = operand1 in (operand1 for var in variables)
                operand2 = float(operand2)
                if cond1:
                    memory.update({variable: operand2 + memory[operand1]})
            else:
                call_error("Incorrect use of +")
        elif word == '-':
            line_process = 1
            variable = words[idx - 3]
            variables.append(variable)
            operand1 = words[idx - 1]
            operand2 = words[idx + 1]
            if operand1.isalpha() and operand2.isalpha():
                cond1, cond2 = False, False
                for var in variables:
                    if operand1 == var:
                        cond1 = True
                    if operand2 == var:
                        cond2 = True
                if cond2 and cond1:
                    memory.update({variable: memory[operand1] - memory[operand2]})
                else:
                    if cond1:
                        var = operand2
                    else:
                        var = operand1
                    error = "Variable not declared: " + str(var)
                    call_error(error)
            elif operand1.isnumeric() and operand2.isalpha():
                cond1 = operand2 in (operand2 for var in variables)
                operand1 = float(operand1)
                if cond1:
                    memory.update({variable: operand1 - memory[operand2]})
            elif operand2.isnumeric() and operand1.isalpha():
                cond1 = operand1 in (operand1 for var in variables)
                operand2 = float(operand2)
                if cond1:
                    memory.update({variable: memory[operand1] - operand2})
            else:
                call_error("Incorrect use of -")
        elif word == '*':
            print(idx)
            line_process = 1
            variable = words[idx - 3]
            variables.append(variable)
            operand1 = words[idx - 1]
            operand2 = words[idx + 1]
            if operand1.isalpha() and operand2.isalpha():
                cond1, cond2 = False, False
                for var in variables:
                    if operand1 == var:
                        cond1 = True
                    if operand2 == var:
                        cond2 = True
                if cond2 and cond1:
                    memory.update({variable: memory[operand1] * memory[operand2]})
                else:
                    if cond1:
                        var = operand2
                    else:
                        var = operand1
                    error = "Variable not declared: " + str(var)
                    call_error(error)
            elif operand1.isnumeric() and operand2.isalpha():
                cond1 = operand2 in (operand2 for var in variables)
                operand1 = float(operand1)
                if cond1:
                    memory.update({variable: operand1 * memory[operand2]})
            elif operand2.isnumeric() and operand1.isalpha():
                cond1 = operand1 in (operand1 for var in variables)
                operand2 = float(operand2)
                if cond1:
                    memory.update({variable: memory[operand1] * operand2})
            else:
                call_error("Incorrect use of *")
        elif word == '/':
            line_process = 1
            variable = words[idx - 3]
            variables.append(variable)
            operand1 = words[idx - 1]
            operand2 = words[idx + 1]
            if operand1.isalpha() and operand2.isalpha():
                cond1, cond2 = False, False
                for var in variables:
                    if operand1 == var:
                        cond1 = True
                    if operand2 == var:
                        cond2 = True
                if memory[operand2] != 0:
                    if cond2 and cond1:
                        memory.update({variable: memory[operand1] / memory[operand2]})
                    else:
                        if cond1:
                            var = operand2
                        else:
                            var = operand1
                        error = "Variable not declared: " + str(var)
                        call_error(error)
                else:
                    call_error("Zero divide error")
            elif operand1.isnumeric() and operand2.isalpha():
                cond1 = operand2 in (operand2 for var in variables)
                operand1 = float(operand1)
                if cond1:
                    memory.update({variable: operand1 / memory[operand2]})
            elif operand2.isnumeric() and operand1.isalpha():
                cond1 = operand1 in (operand1 for var in variables)
                operand2 = float(operand2)
                if cond1:
                    memory.update({variable: memory[operand1] * operand2})
            else:
                call_error("Incorrect use of /")
        elif word == '**':
            line_process = 1
            variable = words[idx - 3]
            variables.append(variable)
            operand1 = words[idx - 1]
            operand2 = words[idx + 1]
            if operand1.isalpha() and operand2.isalpha():
                cond1, cond2 = False, False
                for var in variables:
                    if operand1 == var:
                        cond1 = True
                    if operand2 == var:
                        cond2 = True
                if cond2 and cond1:
                    memory.update({variable: memory[operand1] ** memory[operand2]})
                else:
                    if cond1:
                        var = operand2
                    else:
                        var = operand1
                    error = "Variable not declared: " + str(var)
                    call_error(error)
            elif operand1.isnumeric() and operand2.isalpha():
                cond1 = operand2 in (operand2 for var in variables)
                operand1 = float(operand1)
                if cond1:
                    memory.update({variable: operand1 ** memory[operand2]})
            elif operand2.isnumeric() and operand1.isalpha():
                cond1 = operand1 in (operand1 for var in variables)
                operand2 = float(operand2)
                if cond1:
                    memory.update({variable: memory[operand1] ** operand2})
            else:
                call_error("Incorrect use of **")
        elif word == "actuator_write":
            pass
        elif word == "mat":
            line_process = 1
            idx = idx + 1
            variable = words[idx]
            idx = idx + 2
            operand1 = words[idx]
            idx = idx + 2
            operand2 = words[idx]
            operation = words[idx-1]
            if operation in matrix_operations:
                flag1 = 0
                flag2 = 0
                flag3 = 0
                for var in variables:
                    if variable == var:
                        flag1 = 1
                    elif operand1 == var:
                        flag2 = 1
                    elif operand2 == var:
                        flag3 = 1
                condition = flag1 + flag2 + flag3
                if condition == 3:
                    if operation == '*':
                        mat1 = np.array(memory[operand1])
                        mat2 = np.array(memory[operand2])

                        try:
                            result = np.dot(mat1, mat2)
                            if result.shape == np.array(memory[variable]).shape:
                                memory[variable] = result.tolist()
                            else:
                                call_error("Shape mismatch between arrays: Trying to assign " + str(result.shape) + " to " + str(np.array(memory[variable]).shape))
                        except ValueError:
                            call_error("Shape mismatch between arrays: Trying to multiply " + str(mat1.shape) + ' with '+str(mat2.shape))
                    elif operation == '.*':
                        mat1 = np.array(memory[operand1])
                        mat2 = np.array(memory[operand2])

                        try:
                            result = np.multiply(mat1, mat2)
                            if result.shape == np.array(memory[variable]).shape:
                                memory[variable] = result.tolist()
                            else:
                                call_error("Shape mismatch between arrays: Trying to assign " + str(result.shape) + " to " + str(np.array(memory[variable]).shape))
                        except ValueError:
                            call_error("Shape mismatch between arrays: Trying to element wise multiply " + str(mat1.shape) + ' with '+str(mat2.shape))
                elif condition == 2 and flag3 == 0:
                    if operation == "'":
                        mat = np.array(memory[operand1])
                        try:
                            result = np.transpose(mat)
                            if result.shape == np.array(memory[variable]).shape:
                                memory[variable] = result.tolist()
                            else:
                                call_error(
                                    "Shape mismatch between arrays: Trying to assign " + str(result.shape) + " to " + str(
                                        np.array(memory[variable]).shape))
                        except ValueError:
                            call_error("Shape mismatch between arrays")
                    if operation == "^":
                        if operand2 == '-1':
                            mat = np.array(memory[operand1])
                            try:
                                result = np.linalg.inv(mat)
                                if result.shape == np.array(memory[variable]).shape:
                                    memory[variable] = result.tolist()
                                else:
                                    call_error(
                                        "Shape mismatch between arrays: Trying to assign " + str(result.shape) + " to " + str(
                                            np.array(memory[variable]).shape))
                            except ValueError:
                                call_error("Non Invertible matrix")
                        if operand2.isnumeric():
                            mat = np.array(memory[operand1])
                            try:
                                result = np.eye(mat.shape[0])
                                for i in range(int(operand2)):
                                    result = np.dot(result, mat)
                                result = mat
                                if result.shape == np.array(memory[variable]).shape:
                                    memory[variable] = result.tolist()
                                else:
                                    call_error(
                                        "Shape mismatch between arrays: Trying to assign " + str(result.shape) + " to " + str(
                                            np.array(memory[variable]).shape))
                            except ValueError:
                                call_error("Shape error: Requires a square matrix given shape "+str(result.shape))
                else:
                    if not flag1:
                        var = variable
                    elif not flag2:
                        var = operand1
                    elif not flag3:
                        var = operand2
                    error = "Variable not Initiated: " + str(var)
                    call_error(error)
            else:
                call_error("Trying Invalid Operations")

        idx = idx + 1

    print('\n')
    print("Memory: ", memory)
