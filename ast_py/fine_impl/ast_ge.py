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
            children.append(self.traverse(item))
        if children:
            json_node["children"] = children
        return pos

    @staticmethod
    def is_try(node):
        return hasattr(ast, "Try") and isinstance(node, ast.Try) or \
               hasattr(ast, "TryExcept") and isinstance(node, ast.TryExcept) or \
               hasattr(ast, "TryFinally") and isinstance(node, ast.TryFinally)

    def traverse(self, node):
        pos = len(self._nodes)
        json_node = {"id": pos}
        self._nodes.append(json_node)
        json_node["type"] = type(node).__name__
        children = []
        if isinstance(node, (ast.DictComp, ast.SetComp, ast.ListComp, ast.GeneratorExp)):
            pass
        elif isinstance(node, ast.For):
            json_node["type"] = "for"
            children.append(self.traverse(node.target))
            children.append(self.traverse(node.iter))
            children.append(self.traverse_list(node.body, "block"))
            if node.orelse:
                children.append(self.traverse_list(node.orelse, "block"))
        elif isinstance(node, ast.If):
            json_node["type"] = "if"
            children.append(self.traverse(node.test))
            children.append(self.traverse_list(node.body, "block"))
            if node.orelse:
                children.append(self.traverse_list(node.orelse, "block"))
        elif isinstance(node, ast.While):
            json_node["type"] = "while"
            children.append(self.traverse(node.test))
            children.append(self.traverse_list(node.body, "block"))
            if node.orelse:
                children.append(self.traverse_list(node.orelse, "block"))
        elif isinstance(node, ast.Module):
            json_node["type"] = "root"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.Attribute):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.expr_context)):
                    json_node["type"] = json_node["type"] + type(child).__name__
                else:
                    children.append(self.traverse(child))
        elif isinstance(node, ast.Name):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.expr_context)):
                    json_node["type"] = json_node["type"] + type(child).__name__
                    if json_node["type"] == "NameLoad":
                        json_node["type"] = "identifier"
                    if json_node["type"] == "NameStore":
                        json_node["type"] = "var"
                    if json_node["type"] == "NameConstant":
                        json_node["type"] = "constant"
                else:
                    children.append(self.traverse(child))
        elif isinstance(node, (ast.expr_context, ast.operator, ast.boolop, ast.unaryop, ast.cmpop)):
            pass
        elif isinstance(node, ast.Subscript):
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
                    children.append(self.traverse(child.value))
                else:
                    children.append(self.traverse(child))
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes, ast.NameConstant, ast.Ellipsis)):
            json_node["type"] = "constant"
        elif isinstance(node, ast.Call):
            json_node["type"] = "call"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            json_node["type"] = "assignment"
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.operator, ast.boolop, ast.unaryop, ast.cmpop)):
                    pass
                else:
                    children.append(self.traverse(child))
        elif isinstance(node, (ast.Compare, ast.BinOp, ast.BoolOp, ast.UnaryOp)):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Eq):
                    json_node["type"] = "equal"
                elif isinstance(child, ast.NotEq):
                    json_node["type"] = "notequal"
                elif isinstance(child, ast.Lt):
                    json_node["type"] = "lt"
                elif isinstance(child, ast.LtE):
                    json_node["type"] = "lte"
                elif isinstance(child, ast.Gt):
                    json_node["type"] = "gt"
                elif isinstance(child, ast.GtE):
                    json_node["type"] = "gte"
                elif isinstance(child, ast.Is):
                    json_node["type"] = "is"
                elif isinstance(child, ast.IsNot):
                    json_node["type"] = "isnot"
                elif isinstance(child, ast.In):
                    json_node["type"] = "in"
                elif isinstance(child, ast.NotIn):
                    json_node["type"] = "notin"
                elif isinstance(child, ast.Add):
                    json_node["type"] = "add"
                elif isinstance(child, ast.Sub):
                    json_node["type"] = "sub"
                elif isinstance(child, ast.Mult):
                    json_node["type"] = "multiply"
                elif isinstance(child, ast.Div):
                    json_node["type"] = "divide"
                elif isinstance(child, ast.FloorDiv):
                    json_node["type"] = "floordiv"
                elif isinstance(child, ast.Mod):
                    json_node["type"] = "mod"
                elif isinstance(child, ast.Pow):
                    json_node["type"] = "pow"
                elif isinstance(child, ast.LShift):
                    json_node["type"] = "lshift"
                elif isinstance(child, ast.RShift):
                    json_node["type"] = "rshift"
                elif isinstance(child, ast.BitOr):
                    json_node["type"] = "bitor"
                elif isinstance(child, ast.BitXor):
                    json_node["type"] = "bitxor"
                elif isinstance(child, ast.BitAnd):
                    json_node["type"] = "bitand"
                elif isinstance(child, ast.MatMult):
                    json_node["type"] = "matmul"
                elif isinstance(child, ast.UAdd):
                    json_node["type"] = "uadd"
                elif isinstance(child, ast.USub):
                    json_node["type"] = "usub"
                elif isinstance(child, ast.Not):
                    json_node["type"] = "not"
                elif isinstance(child, ast.Invert):
                    json_node["type"] = "invert"
                elif isinstance(child, ast.And):
                    json_node["type"] = "and"
                elif isinstance(child, ast.Or):
                    json_node["type"] = "or"
                else:
                    children.append(self.traverse(child))
        elif isinstance(node, ast.IfExp):
            json_node["type"] = "ternary"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.Return):
            json_node["type"] = "return"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.ClassDef):
            json_node["type"] = "classdef"
            children.append(self.traverse_list(node.body, "block"))
        elif isinstance(node, ast.FunctionDef):
            json_node["type"] = "funcdef"
            json_node["value"] = node.name
            children.append(self.traverse(node.args))
            children.append(self.traverse_list(node.body, "block"))
        elif isinstance(node, ast.Continue):
            json_node["type"] = "continue"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.Break):
            json_node["type"] = "break"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.Assert):
            json_node["type"] = "assert"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.Raise):
            json_node["type"] = "throw"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.ExceptHandler):
            json_node["type"] = "catch"
            children.append(self.traverse_list(node.body, "block"))
        elif self.is_try(node):
            json_node["type"] = "try"
            children.append(self.traverse_list(node.body, "block"))
            if node.handlers:
                for handler in node.handlers:
                    children.append(self.traverse(handler))
            if node.orelse:
                children.append(self.traverse_list(node.orelse, "block"))
            if node.finalbody:
                children.append(self.traverse_list(node.finalbody, "block"))
        elif isinstance(node, ast.With):  # TODO
            json_node["type"] = "with"
            # if hasattr(node, "context_expr"):
            #     children.append(self.traverse(node.context_expr))
            # else:
            #     children.append(self.traverse_list(node.items))
            # if getattr(node, "optional_vars", None):
            #     children.append(self.traverse(node.optional_vars))
            children.append(self.traverse_list(node.body, "block"))
        # elif hasattr(ast, "withitem") and isinstance(node, ast.withitem):  # TODO
        #     children.append(self.traverse(node.context_expr))
        #     if node.optional_vars:
        #         children.append(self.traverse(node.optional_vars))
        elif isinstance(node, ast.arguments):
            json_node["type"] = "param"
            if node.args:
                for arg in node.args:
                    children.append(self.traverse(arg))
            if node.vararg and isinstance(node.vararg, str):
                children.append(self.gen_identifier(node.vararg, "vararg"))
            if node.kwarg and isinstance(node.kwarg, str):
                children.append(self.gen_identifier(node.kwarg, "kwarg"))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            json_node["type"] = "import"
        elif isinstance(node, ast.Lambda):
            json_node["type"] = "lambda"
            for child in ast.iter_child_nodes(node):
                children.append(self.traverse(child))
        elif isinstance(node, ast.Expr):
            for child in ast.iter_child_nodes(node):
                return self.traverse(child)
        # elif isinstance(node, ast.Index):
        #     for child in ast.iter_child_nodes(node):
        #         json_node["type"] = type(child).__name__
        # elif isinstance(node, ast.Tuple):
        #     for child in ast.iter_child_nodes(node):
        #         if isinstance(child, (ast.expr_context)):
        #             json_node["type"] = json_node["type"] + type(child).__name__
        #         else:
        #             children.append(self.traverse(child))
        else:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.expr_context)):
                    json_node["type"] = json_node["type"] + type(child).__name__
                else:
                    children.append(self.traverse(child))

        if children:
            json_node["children"] = children

        return pos
