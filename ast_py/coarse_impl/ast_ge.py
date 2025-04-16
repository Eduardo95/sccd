import ast
from ast_py.utils import normalizer
unicode = str
decode_utf8 = lambda x: x


def parse_file(filename, normalize=False):
    with open(filename, "r") as f:
        content = f.read()
    return ASTGenerator(content, normalize=normalize).generate_ast()


class ASTGenerator:
    def __init__(self, content, filename="<unknonwn>", normalize=False):
        self.content = content
        self.tree = ast.parse(self.content, filename)
        if normalize:
            self.tree = normalizer.normalize(self.tree)
        self._nodes = []

    def generate_ast(self):
        self._nodes = []
        self.traverse(self.tree)
        return self._nodes

    def gen_identifier(self, identifier, node_type="identifier"):
        pos = len(self._nodes)
        json_node = {"id": pos}
        self._nodes.append(json_node)
        json_node["type"] = node_type
        json_node["value"] = identifier
        return pos

    def traverse_list(self, nodes_list, node_type="list"):
        pos = len(self._nodes)
        json_node = {"id": pos}
        self._nodes.append(json_node)
        json_node["type"] = node_type
        children = []
        for item in nodes_list:
            tmp = self.traverse(item)
            if tmp:
                children.append(tmp)
        if children:
            json_node["children"] = children
        return pos

    @staticmethod
    def is_try(node):
        return hasattr(ast, "Try") and isinstance(node, ast.Try) or \
               hasattr(ast, "TryExcept") and isinstance(node, ast.TryExcept) or \
               hasattr(ast, "TryFinally") and isinstance(node, ast.TryFinally)

    def traverse(self, node):
        if isinstance(node, ast.Module):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "root"
            children = []
            for child in ast.iter_child_nodes(node):
                tmp = self.traverse(child)
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.ClassDef):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "classdef"
            children = [self.traverse_list(node.body, "block")]
            json_node["children"] = children
            return pos
        elif isinstance(node, ast.FunctionDef):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "funcdef"
            json_node["value"] = node.name
            children = []
            tmp = self.traverse(node.args)
            if tmp:
                children.append(tmp)
            children.append(self.traverse_list(node.body, "block"))
            json_node["children"] = children
            return pos
        elif isinstance(node, (ast.DictComp, ast.SetComp, ast.ListComp, ast.GeneratorExp)):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "for"
            return pos
        elif isinstance(node, ast.For):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "for"
            children = [self.traverse_list([], "condition"), self.traverse_list(node.body, "block")]
            json_node["children"] = children
            return pos
        elif isinstance(node, ast.If):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "if"
            children = [self.traverse_list([], "condition"), self.traverse_list(node.body, "block")]
            if node.orelse:
                children.append(self.traverse_list(node.orelse, "block"))
            json_node["children"] = children
            return pos
        elif isinstance(node, ast.While):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "while"
            children = [self.traverse_list([], "condition"), self.traverse_list(node.body, "block")]
            json_node["children"] = children
            return pos
        elif isinstance(node, ast.Attribute):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "Attribute"
            children = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.Load)):
                    json_node["type"] = json_node["type"] + type(child).__name__
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.Name):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "Name"
            children = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.expr_context)):
                    json_node["type"] = json_node["type"] + type(child).__name__
                    if json_node["type"] == "NameLoad":
                        json_node["type"] = "identifier"
                    if json_node["type"] == "NameStore":
                        json_node["type"] = "var"
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, (ast.expr_context, ast.operator, ast.boolop, ast.cmpop)):
            pass
        elif isinstance(node, ast.Subscript):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "Subscript"
            children = []

            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.expr_context)):
                    json_node["type"] = json_node["type"] + type(child).__name__
                    if json_node["type"] == "SubscriptLoad":
                        json_node["type"] = "arrayaccess"
                    if json_node["type"] == "SubscriptStore":
                        json_node["type"] = "arrayaccess"
                    if json_node["type"] == "SubscriptDel":
                        json_node["type"] = "arrayaccess"
                elif isinstance(child, ast.Index):
                    tmp = self.traverse(child.value)
                    if tmp:
                        children.append(tmp)
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes, ast.NameConstant, ast.Ellipsis)):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "constant"
            return pos
        elif isinstance(node, ast.Call):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "call"
            children = []
            for child in ast.iter_child_nodes(node):
                tmp = self.traverse(child)
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "assignment"
            children = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.operator, ast.boolop, ast.unaryop, ast.cmpop)):
                    pass
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, (ast.Compare, ast.BinOp, ast.BoolOp)):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "binaryop"
            children = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.operator, ast.boolop, ast.cmpop)):
                    pass
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.UnaryOp):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "unaryop"
            children = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.unaryop)):
                    pass
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.IfExp):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "ternary"
            return pos
        elif isinstance(node, ast.Return):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "return"
            return pos
        elif isinstance(node, ast.Continue):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "continue"
            return pos
        elif isinstance(node, ast.Break):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "break"
            return pos
        elif isinstance(node, ast.Assert):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "assert"
            return pos
        elif isinstance(node, ast.Raise):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "throw"
            return pos
        elif isinstance(node, ast.ExceptHandler):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "catch"
            children = [self.traverse_list(node.body, "block")]
            json_node["children"] = children
            return pos
        elif self.is_try(node):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "try"
            children = [self.traverse_list(node.body, "block")]
            if node.handlers:
                for handler in node.handlers:
                    tmp = self.traverse(handler)
                    if tmp:
                        children.append(tmp)
            if node.orelse:
                children.append(self.traverse_list(node.orelse, "block"))
            if node.finalbody:
                children.append(self.traverse_list(node.finalbody, "block"))
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.With):
            pass
        elif isinstance(node, ast.arguments):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "param"
            children = []
            if node.args:
                for arg in node.args:
                    tmp = self.traverse(arg)
                    if tmp:
                        children.append(tmp)
            if node.vararg and isinstance(node.vararg, str):
                children.append(self.gen_identifier(node.vararg, "vararg"))
            if node.kwarg and isinstance(node.kwarg, str):
                children.append(self.gen_identifier(node.kwarg, "kwarg"))
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, (ast.ImportFrom, ast.Import)):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "import"
            return pos
        elif isinstance(node, ast.Lambda):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "funcdef"
            json_node["value"] = "lambda"
            children = []
            for child in ast.iter_child_nodes(node):
                tmp = self.traverse(child)
                if tmp:
                    children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.Expr):
            for child in ast.iter_child_nodes(node):
                return self.traverse(child)
            return
        elif isinstance(node, ast.Tuple):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Load):
                    return self.traverse_list([], "identifier")
                elif isinstance(child, ast.Store):
                    return self.traverse_list([], "var")
                else:
                    pass
            return
        elif isinstance(node, ast.List):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "List"
            children = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Load):
                    json_node["type"] = json_node["type"] + type(child).__name__
                else:
                    tmp = self.traverse(child)
                    if tmp:
                        children.append(tmp)
            if children:
                json_node["children"] = children
            return pos
        elif isinstance(node, ast.arg):
            pos = len(self._nodes)
            json_node = {"id": pos}
            self._nodes.append(json_node)
            json_node["type"] = "arg"
            return pos
        else:
            pass
        return
