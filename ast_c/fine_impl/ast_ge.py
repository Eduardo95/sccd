from pycparser import parse_file as pf
from pycparser import c_ast


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_binary_operator(s):
    if s == "&&":
        return "and"
    elif s == "||":
        return "or"
    elif s == "+":
        return "add"
    elif s == "-":
        return "sub"
    elif s == "*":
        return "multiply"
    elif s == "/":
        return "divide"
    elif s == "<<":
        return "lshift"
    elif s == ">>":
        return "rshift"
    elif s == "|":
        return "bitor"
    elif s == "^":
        return "bitxor"
    elif s == "&":
        return "bitand"
    elif s == "==":
        return "equal"
    elif s == "!=":
        return "notequal"
    elif s == "<":
        return "lt"
    elif s == "<=":
        return "lte"
    elif s == ">":
        return "gt"
    elif s == ">=":
        return "gte"
    elif s == "%":
        return "remainder"
    return ""


def get_unary_operator(s):
    if s == "~":
        return "invert"
    elif s == "!":
        return "not"
    elif s == "+":
        return "uadd"
    elif s == "-":
        return "usub"
    elif s == "++":
        return "increment"
    elif s == "--":
        return "decrement"
    elif s == "&":
        return "addressof"
    elif s == "*":
        return "dereference"
    elif s == "p++":
        return "increment"
    elif s == "p--":
        return "decrement"
    elif s == "sizeof":
        return "sizeof"
    return ""


class ASTGenerator:
    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self._nodes = []

    def generate_ast(self):
        self._nodes = []
        self.traverse(self.tree)
        return self._nodes

    def traverse_list(self, nodes_list, node_type):
        pos = len(self._nodes)
        json_node = {"id": pos}
        self._nodes.append(json_node)
        json_node["type"] = node_type
        children = []
        for item in nodes_list:
            children.append(self.traverse(item[1]))
        if children:
            json_node["children"] = children
        return pos

    def traverse(self, node):
        pos = len(self._nodes)
        json_node = {"id": pos}
        self._nodes.append(json_node)
        json_node["type"] = node.__class__.__name__
        children = []

        # done
        if isinstance(node, c_ast.ArrayRef):
            json_node["type"] = "arrayaccess"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Assignment):
            json_node["type"] = "assignment"
            if node.op:
                json_node["value"] = node.op
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Alignas):
            json_node["type"] = "alignas"
        # done
        if isinstance(node, c_ast.BinaryOp):
            if node.op:
                json_node["type"] = get_binary_operator(node.op)
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Break):
            json_node["type"] = "break"
        # done
        if isinstance(node, c_ast.Case):
            json_node["type"] = "case"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Cast):
            json_node["type"] = "cast"
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.Typename):
                    children.append(self.traverse(stmt[1].children()[0][1]))
                else:
                    children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Compound):
            json_node["type"] = "block"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Constant):
            json_node["type"] = "constant"
            val = node.value
            if is_numeric(val):
                if is_int(val):
                    json_node["value"] = int(val)
                else:
                    json_node["value"] = float(val)
            else:
                json_node["value"] = val
        # done
        if isinstance(node, c_ast.Continue):
            json_node["type"] = "continue"
        # done
        if isinstance(node, c_ast.DoWhile):
            json_node["type"] = "dowhile"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.FileAST):
            json_node["type"] = "root"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.While):
            json_node["type"] = "while"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.UnaryOp):
            if node.op:
                json_node["type"] = get_unary_operator(node.op)
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.Typename):
                    children.append(self.traverse(stmt[1].children()[0][1]))
                else:
                    children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.If):
            json_node["type"] = "if"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.TernaryOp):
            json_node["type"] = "ternary"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Return):
            json_node["type"] = "return"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.For):
            json_node["type"] = "for"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.FuncCall):
            json_node["type"] = "call"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.FuncDef):
            json_node["type"] = "funcdef"
            json_node["value"] = node.decl.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Goto):
            json_node["type"] = "goto"
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.EllipsisParam):
            json_node["type"] = "param"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.ID):
            json_node["type"] = "identifier"
            if node.name:
                json_node["value"] = node.name
        # done
        if isinstance(node, c_ast.Switch):
            json_node["type"] = "switch"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.Union):
            json_node["type"] = "type"
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.InitList):
            json_node["type"] = "ListLoad"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.IdentifierType):
            json_node["type"] = "type"
            if node.names[0]:
                json_node["value"] = node.names[0]
        # done
        if isinstance(node, c_ast.FuncDecl):
            json_node["type"] = "funcdec"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.ArrayDecl):
            json_node["type"] = "arraydec"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.PtrDecl):
            json_node["type"] = "pointer"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        # done
        if isinstance(node, c_ast.StaticAssert):
            json_node["type"] = "assert"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))

        if isinstance(node, c_ast.CompoundLiteral):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))

        if isinstance(node, c_ast.DeclList):
            json_node["type"] = "expression"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.ExprList):
            json_node["type"] = "expression"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))

        if isinstance(node, c_ast.Decl):
            if isinstance(node.children()[0][1], c_ast.PtrDecl):
                json_node["type"] = "pointer"
                children.append(self.traverse(node.children()[0][1].children()[0][1]))
            elif isinstance(node.children()[0][1], c_ast.FuncDecl):
                json_node["type"] = "funcdec"
                for stmt in node.children()[0][1].children():
                    children.append(self.traverse(stmt[1]))
            elif isinstance(node.children()[0][1], c_ast.ArrayDecl):
                json_node["type"] = "arraydec"
                for stmt in node.children()[0][1].children():
                    children.append(self.traverse(stmt[1]))
            elif isinstance(node.children()[0][1], c_ast.TypeDecl) and isinstance(node.children()[0][1].children()[0][1], c_ast.IdentifierType):
                json_node["type"] = "var"
                if node.name:
                    json_node["value"] = node.name
                for stmt in node.children():
                    children.append(self.traverse(stmt[1]))
            else:
                if node.name:
                    json_node["value"] = node.name
                for stmt in node.children():
                    children.append(self.traverse(stmt[1]))

        if isinstance(node, c_ast.TypeDecl):
            if isinstance(node.children()[0][1], c_ast.IdentifierType):
                json_node["type"] = "type"
                if node.children()[0][1].names[0]:
                    json_node["value"] = node.children()[0][1].names[0]
            else:
                json_node["type"] = node.children()[0][1].__class__.__name__
                for stmt in node.children()[0][1].children():
                    children.append(self.traverse(stmt[1]))

        if isinstance(node, c_ast.Default):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.EmptyStatement):
            json_node["type"] = "empty"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Enum):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Enumerator):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.EnumeratorList):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Label):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.NamedInitializer):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Struct):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.StructRef):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Pragma):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Typedef):
            json_node["type"] = "typedef"
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.ParamList):
            json_node["type"] = "param"
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.Typename):
                    children.append(self.traverse_list(stmt[1].children(), "arg"))
                    # children.append(self.traverse(stmt[1].children()[0][1]))
                elif isinstance(stmt[1], c_ast.Decl):
                    children.append(self.traverse_list(stmt[1].children(), "arg"))
                elif isinstance(stmt[1], c_ast.ID):
                    children.append(self.traverse_list(stmt[1].children(), "arg"))

        if isinstance(node, c_ast.Typename):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))


        if children:
            json_node["children"] = children
        return pos


def parse_file(filename):
    # ast = pf(filename, use_cpp=True, cpp_path='gcc')
    ast = pf(filename, use_cpp=True, cpp_path='gcc', cpp_args=['-E', r'-I/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_c/fake_libc_include'])
    return ASTGenerator(ast, filename).generate_ast()


a = parse_file("/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_c/bubble.c")
print(a)