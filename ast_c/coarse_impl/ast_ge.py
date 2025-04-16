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
            tmp = self.traverse(item[1])
            if tmp:
                children.append(tmp)
        if children:
            json_node["children"] = children
        return pos

    def traverse(self, node):
        # done
        if isinstance(node, c_ast.FileAST):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "root"
            children = []
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.ArrayRef):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "arrayaccess"
            children = []
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.Alignas):
            pass
        # done
        elif isinstance(node, c_ast.Break):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "break"
            return pos
        # done
        elif isinstance(node, c_ast.Cast):
            pass
        # done
        elif isinstance(node, c_ast.Continue):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "continue"
            return pos
        # done
        elif isinstance(node, c_ast.Assignment):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "assignment"
            children = []
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.BinaryOp):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "binaryop"
            children = []
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.Case):
            pass
        # done
        elif isinstance(node, c_ast.Compound):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "block"
            children = []
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.ExprList):
                    for tmp in stmt[1].children():
                        tmp_1 = self.traverse(tmp[1])
                        if tmp_1:
                            children.append(tmp_1)
                else:
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.Constant):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "constant"
            return pos
        # done
        elif isinstance(node, c_ast.DoWhile):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "while"
            children = [self.traverse_list([], "condition")]
            if node.stmt:
                if isinstance(node.stmt, c_ast.ExprList):
                    children.append(self.traverse_list(node.stmt.children(), "block"))
                else:
                    tmp = self.traverse(node.stmt)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.While):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "while"
            children = [self.traverse_list([], "condition")]
            if node.stmt:
                if isinstance(node.stmt, c_ast.ExprList):
                    children.append(self.traverse_list(node.stmt.children(), "block"))
                else:
                    tmp = self.traverse(node.stmt)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.UnaryOp):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "unaryop"
            children = []
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.Typename):
                    tmp = self.traverse(stmt[1].children()[0][1])
                    if tmp:
                        children.append(tmp)
                else:
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.CompoundLiteral):
            pass
        # done
        elif isinstance(node, c_ast.If):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "if"
            children = [self.traverse_list([], "condition")]
            if node.iftrue:
                if isinstance(node.iftrue, c_ast.ExprList):
                    children.append(self.traverse_list(node.iftrue.children(), "block"))
                else:
                    tmp = self.traverse(node.iftrue)
                    if tmp:
                        children.append(tmp)
            if node.iffalse:
                if isinstance(node.iffalse, c_ast.ExprList):
                    children.append(self.traverse_list(node.iffalse.children(), "block"))
                else:
                    tmp = self.traverse(node.iffalse)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.TernaryOp):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "ternary"
            return pos
        # done
        elif isinstance(node, c_ast.Return):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "return"
            return pos
        # done
        elif isinstance(node, c_ast.For):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "for"
            children = [self.traverse_list([], "condition")]
            if node.stmt:
                if isinstance(node.stmt, c_ast.ExprList):
                    children.append(self.traverse_list(node.stmt.children(), "block"))
                else:
                    tmp = self.traverse(node.stmt)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.FuncCall):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "call"
            children = []
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.ExprList):
                    for stmt_1 in stmt[1].children():
                        tmp = self.traverse(stmt_1[1])
                        if tmp:
                            children.append(tmp)
                else:
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.Goto):
            pass
        # done
        elif isinstance(node, c_ast.ID):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "identifier"
            if node.name:
                json_node["value"] = node.name
            return pos
        # done
        elif isinstance(node, c_ast.Pragma):
            pass
        # done
        elif isinstance(node, c_ast.EmptyStatement):
            pass
        # done
        elif isinstance(node, c_ast.Switch):
            pass
        # done
        elif isinstance(node, c_ast.Union):
            pass
        # done
        elif isinstance(node, c_ast.StaticAssert):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "assert"
            return pos
        # done
        elif isinstance(node, c_ast.Default):
            pass
        # done
        elif isinstance(node, c_ast.Label):
            pass
        # done
        elif isinstance(node, c_ast.Enum):
            pass
        # done
        elif isinstance(node, c_ast.Enumerator):
            pass
        # done
        elif isinstance(node, c_ast.EnumeratorList):
            pass
        # done
        elif isinstance(node, c_ast.NamedInitializer):
            pass
        # done
        elif isinstance(node, c_ast.StructRef):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "AttributeLoad"
            children = []
            if node.name:
                tmp = self.traverse(node.name)
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.EllipsisParam):
            pass
        # done
        elif isinstance(node, c_ast.InitList):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "ListLoad"
            children = []
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.Struct):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "struct"
            children = []
            if node.name:
                json_node["value"] = node.name
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.IdentifierType):
            pass
        # done
        elif isinstance(node, c_ast.FuncDef):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "funcdef"
            json_node["value"] = node.decl.name
            children = []
            if node.decl:
                for stmt in node.decl.type.children():
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            if node.body:
                tmp = self.traverse(node.body)
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.FuncDecl):
            pass
        # done
        elif isinstance(node, c_ast.ArrayDecl):
            pass
        # done
        elif isinstance(node, c_ast.TypeDecl):
            pass
        # done
        elif isinstance(node, c_ast.Typedef):
            pass
        # done
        elif isinstance(node, c_ast.Decl):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "var"
            children = []
            if isinstance(node.children()[0][1], c_ast.PtrDecl):
                tmp = self.traverse(node.children()[0][1].children()[0][1])
                if tmp:
                    children.append(tmp)
            elif isinstance(node.children()[0][1], c_ast.FuncDecl):
                return
            elif isinstance(node.children()[0][1], c_ast.ArrayDecl):
                for stmt in node.children():
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            elif isinstance(node.children()[0][1], c_ast.TypeDecl) and isinstance(node.children()[0][1].children()[0][1], c_ast.IdentifierType):
                if node.name:
                    json_node["value"] = node.name
                for stmt in node.children():
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            else:
                if node.name:
                    json_node["value"] = node.name
                for stmt in node.children():
                    tmp = self.traverse(stmt[1])
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        # done
        elif isinstance(node, c_ast.PtrDecl):
            pass
        # done
        elif isinstance(node, c_ast.Typename):
            pass
        # done
        elif isinstance(node, c_ast.ParamList):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "param"
            children = []
            for stmt in node.children():
                if isinstance(stmt[1], c_ast.Typename):
                    children.append(self.traverse_list([], "arg"))
                elif isinstance(stmt[1], c_ast.Decl):
                    children.append(self.traverse_list([], "arg"))
                elif isinstance(stmt[1], c_ast.ID):
                    children.append(self.traverse_list([], "arg"))
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, c_ast.DeclList):
            pass


        elif isinstance(node, c_ast.ExprList):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = node.__class__.__name__
            children = []
            json_node["type"] = "expression"
            for stmt in node.children():
                tmp = self.traverse(stmt[1])
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        else:
            pass

        return


def parse_file(filename):
    # ast = pf(filename, use_cpp=True, cpp_path='gcc')
    ast = pf(filename, use_cpp=True, cpp_path='gcc', cpp_args=['-E', r'-I/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_c/fake_libc_include'])
    return ASTGenerator(ast, filename).generate_ast()

a = parse_file("/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_c/bubble.c")
print(a)