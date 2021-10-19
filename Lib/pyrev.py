import ast

def isrev(code):
    tree_ast = ast.parse(code)

    is_reversible = True
    nodes = [node for node in ast.walk(tree_ast)]

    for n in nodes:
        if isinstance(n, ast.Assign):
            subNodes = [node for node in ast.walk(n.value)]
            for target in n.targets:
                if not isinstance(target, ast.Name):
                    print("At line: ", target.lineno)
                    print("Multiple assignment is not allowed\n")
                    is_reversible = False           
            for sub_n in subNodes:
                if isinstance(sub_n, ast.Name):
                    if sub_n.id == target.id:
                        print("At line: ", sub_n.lineno)
                        print("The target also appears on the right side of the assignment\n")
                        is_reversible = False
        if isinstance(n, ast.AugAssign):
            subNodes = [node for node in ast.walk(n)]
            div_or_mult = False
            for sub_n in subNodes:
                if isinstance(sub_n, ast.Mult):
                    print("At line: ", n.lineno)
                    print("*= is not allowed\n")
                    div_or_mult = True
                    is_reversible = False
                if isinstance(sub_n, ast.Div):
                    print("At line: ", n.lineno)
                    print("/= is not allowed\n")
                    div_or_mult = True
                    is_reversible = False
            if(not div_or_mult):
                subNodes = [node for node in ast.walk(n.value)]
                done = False
                for sub_n in subNodes:
                    if isinstance(sub_n, ast.Name):
                        print("At line: ", n.lineno)
                        print("There is a variable in the right part of the augmented assignment\n")
                        done = True
                        is_reversible = False
                if(not done):
                    tmp_tree = ast.dump(n.value)
                    val = str(tmp_tree)
                    if val.count("value=") != 1:
                        print("At line: ", n.lineno)
                        print("The value of the augmented assignment must be only one\n")
                        is_reversible = False
                    else:
                        if (not "value=1" in val) or ("op=USub()" in val):
                            print("At line: ", n.lineno)
                            print("The value of the augmented assignment must be '1'\n")
                            is_reversible = False
        if isinstance(n, ast.While):
                print("At line: ", n.lineno)
                print("The while loop is not reversible")
                is_reversible = False
        if isinstance(n, ast.IfExp):
            print("At line: ", n.lineno)
            print("This type of construct is not allowed, please use the standard if else construct\n")
            is_reversible = False
        if isinstance(n, ast.If):
            cond_var = []
            bodyelse_var = []
            tmp_tree = ast.dump(n.test)
            strp = str(tmp_tree)
            strp_save = strp
            while "id='" in strp:
                strp = strp.split("id='",1)[1]
                cond_var.append(strp)
            count = 0
            for s in cond_var:
                s = cond_var[count]
                x = str(s)
                x = x.partition("'")[0]
                cond_var[count] = x
                count += 1
            cond_var = list(set(cond_var))
            subNodes = [node for node in ast.walk(n)]
            for sub_n in subNodes:
                if isinstance(sub_n, ast.Assign):
                    for target in sub_n.targets:
                        bodyelse_var.append(target.id)
                if isinstance(sub_n, ast.AugAssign):
                        bodyelse_var.append(sub_n.target.id)
            bodyelse_var = list(set(bodyelse_var))
            intersect = list(set(bodyelse_var).intersection(cond_var))
            if intersect:
                print("At line: ", n.lineno)
                print("The variable inside the condition of the if statement is changed in the body\nor in the body of the else\n")
                is_reversible = False
        if isinstance(n, ast.For):
            cond_var = []
            bodyelse_var = []
            tmp_tree = ast.dump(n.target)
            strp = str(tmp_tree)
            strp_save = strp
            while "id='" in strp:
                strp = strp.split("id='",1)[1]
                cond_var.append(strp)
            count = 0
            for s in cond_var:
                s = cond_var[count]
                x = str(s)
                x = x.partition("'")[0]
                cond_var[count] = x
                count += 1
            if isinstance(n.iter, ast.Name):
                cond_var.append(n.iter.id)
            cond_var = list(set(cond_var))
            subNodes = [node for node in ast.walk(n)]
            for sub_n in subNodes:
                if isinstance(sub_n, ast.Assign):
                    for target in sub_n.targets:
                        bodyelse_var.append(target.id)
                if isinstance(sub_n, ast.AugAssign):
                        bodyelse_var.append(sub_n.target.id)
            bodyelse_var = list(set(bodyelse_var))
            intersect = list(set(bodyelse_var).intersection(cond_var))
            print(cond_var)
            print(bodyelse_var)
            print(intersect)
            if intersect:
                print("At line: ", n.lineno)
                print("The variable inside the test of the for statement is changed in the body\nor in the body of the else\n")
                is_reversible = False
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                if n.value.func.id != "range":
                    print("At line: ", n.lineno)
                    print("Calling this function is not certain if it is allowed\n")
                    is_reversible = False

    return is_reversible
