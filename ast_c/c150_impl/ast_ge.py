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
        return "And"
    elif s == "||":
        return "Or"
    elif s == "+":
        return "Add"
    elif s == "-":
        return "Sub"
    elif s == "*":
        return "Mult"
    elif s == "/":
        return "Div"
    elif s == "<<":
        return "LShift"
    elif s == ">>":
        return "RShift"
    elif s == "|":
        return "BitOr"
    elif s == "^":
        return "BitXor"
    elif s == "&":
        return "BitAnd"
    elif s == "==":
        return "Eq"
    elif s == "!=":
        return "NotEq"
    elif s == "<":
        return "Lt"
    elif s == "<=":
        return "LtE"
    elif s == ">":
        return "Gt"
    elif s == ">=":
        return "GtE"
    elif s == "%":
        return "Remainder"
    return ""


def get_unary_operator(s):
    if s == "~":
        return "Invert"
    elif s == "!":
        return "Not"
    elif s == "+":
        return "UAdd"
    elif s == "-":
        return "USub"
    elif s == "++":
        return "Increment"
    elif s == "--":
        return "Decrement"
    elif s == "&":
        return "Addressof"
    elif s == "*":
        return "Dereferencing"
    elif s == "p++":
        return "Increment"
    elif s == "p--":
        return "Decrement"
    elif s == "sizeof":
        return "Sizeof"
    return ""


class ASTGenerator:
    def __init__(self, tree):
        self.tree = tree
        self._nodes = []

    def generate_ast(self):
        self._nodes = []
        self.traverse(self.tree)
        return self._nodes

    def traverse(self, node):
        pos = len(self._nodes)
        json_node = {"id": pos}
        self._nodes.append(json_node)
        json_node["type"] = "c_" + node.__class__.__name__
        children = []
        if isinstance(node, c_ast.ArrayDecl):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.ArrayRef):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Assignment):
            json_node["type"] = "Assignment"
            if node.op:
                json_node["value"] = node.op
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Alignas):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.BinaryOp):
            if node.op:
                json_node["type"] = "BinaryOperation" + get_binary_operator(node.op)
                json_node["value"] = node.op
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Break):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Case):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Cast):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Compound):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.CompoundLiteral):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Constant):
            json_node["type"] = "Constant"
            # TODO node.value
            val = node.value
            if is_numeric(val):
                if is_int(val):
                    json_node["value"] = int(val)
                else:
                    json_node["value"] = float(val)
            else:
                json_node["value"] = val
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Continue):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Decl):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))

        if isinstance(node, c_ast.DeclList):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Default):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.DoWhile):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.EllipsisParam):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.EmptyStatement):
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
        if isinstance(node, c_ast.ExprList):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.FileAST):
            json_node["type"] = "Root"
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.For):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.FuncCall):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.FuncDecl):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.FuncDef):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Goto):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.ID):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.IdentifierType):
            # TODO
            if node.names[0]:
                json_node["value"] = node.names[0]
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.If):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.InitList):
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
        if isinstance(node, c_ast.ParamList):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.PtrDecl):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Return):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.StaticAssert):
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
        if isinstance(node, c_ast.Switch):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.TernaryOp):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.TypeDecl):
            if node.declname:
                json_node["value"] = node.declname
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Typedef):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Typename):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.UnaryOp):
            if node.op:
                json_node["type"] = "UnaryOperation" + get_unary_operator(node.op)
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Union):
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.While):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if isinstance(node, c_ast.Pragma):
            for stmt in node.children():
                children.append(self.traverse(stmt[1]))
        if children:
            json_node["children"] = children
        return pos


def parse_file(filename):
    # ast = pf(filename, use_cpp=True, cpp_path='gcc')
    ast = pf(filename, use_cpp=True, cpp_path='gcc', cpp_args=['-E', r'-I/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_c/fake_libc_include'])
    return ASTGenerator(ast).generate_ast()

#
# a = parse_file("/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_c/bubble.c")
# print(a)