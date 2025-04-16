import javalang
from javalang import tree as jtree


def get_first_method_node(compilation_unit):
    if compilation_unit and compilation_unit.types and compilation_unit.types[0].body:
        if isinstance(compilation_unit.types[0].body[0], jtree.MethodDeclaration) or isinstance(compilation_unit.types[0].body[0], jtree.ConstructorDeclaration):
            return compilation_unit.types[0].body[0]
    return None


def parse_file(file_name, wrap_class=False):
    with open(file_name, "r") as f:
        contents = f.read()
    if wrap_class:
        source = "public class TEMP_CLASS  { %s }" % contents
    else:
        source = contents
    return parse_java(source, wrap_class)


def parse_java(source, wrap_class=False):
    try:
        tree = javalang.parse.parse(source)
    except javalang.parser.JavaSyntaxError:
        return None
    if wrap_class:
        tree = get_first_method_node(tree)
    print(tree)
    return ASTGenerator(tree).generate_ast()


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
        json_node["type"] = node.__class__.__name__
        children = []
        if isinstance(node, jtree.CompilationUnit):
            if node.types:
                for typ in node.types:
                    children.append(self.traverse(typ))
        if isinstance(node, jtree.Literal):
            # append value to node
            json_node["value"] = node.value

        if isinstance(node, jtree.ClassDeclaration):
            json_node["value"] = node.name

            body_pos = len(self._nodes)
            children.append(body_pos)
            # BlockStatement?
            body_json_node = {"id": body_pos, "type": "body"}
            self._nodes.append(body_json_node)
            body_children = []
            if node.body:
                for childd in node.body:
                    body_children.append(self.traverse(childd))
            body_json_node["children"] = body_children
        if isinstance(node, jtree.InterfaceDeclaration):
            # do nothing
            pass
        if isinstance(node, jtree.ClassCreator):
            if node.type:
                children.append(self.traverse(node.type))
            if node.arguments:
                arg_pos = len(self._nodes)
                children.append(arg_pos)
                arg_json_node = {"id": arg_pos, "type": "arguments"}
                self._nodes.append(arg_json_node)
                arg_children = []
                for arg in node.arguments:
                    arg_children.append(self.traverse(arg))
                arg_json_node["children"] = arg_children

            if node.body:
                body_pos = len(self._nodes)
                children.append(body_pos)
                body_json_node = {"id": body_pos, "type": "body"}
                self._nodes.append(body_json_node)
                body_children = []
                for stmt in node.body:
                    body_children.append(self.traverse(stmt))
                body_json_node["children"] = body_children
        if isinstance(node, jtree.InnerClassCreator):
            if node.arguments:
                arg_pos = len(self._nodes)
                children.append(arg_pos)
                arg_json_node = {"id": arg_pos, "type": "arguments"}
                self._nodes.append(arg_json_node)
                arg_children = []
                for arg in node.arguments:
                    arg_children.append(self.traverse(arg))
                arg_json_node["children"] = arg_children

            if node.body:
                body_pos = len(self._nodes)
                children.append(body_pos)
                body_json_node = {"id": body_pos, "type": "body"}
                self._nodes.append(body_json_node)
                body_children = []
                for stmt in node.body:
                    body_children.append(self.traverse(stmt))
                body_json_node["children"] = body_children
        if isinstance(node, (jtree.MethodDeclaration, jtree.ConstructorDeclaration)):
            json_node["value"] = node.name

            parameters_pos = len(self._nodes)
            children.append(parameters_pos)
            parameters_json_node = {"id": parameters_pos, "type": "parameters"}
            self._nodes.append(parameters_json_node)
            parameters_children = []
            for parameter in node.parameters:
                parameters_children.append(self.traverse(parameter))
            parameters_json_node["children"] = parameters_children

            if node.body:
                body_pos = len(self._nodes)
                children.append(body_pos)
                body_json_node = {"id": body_pos, "type": "body"}
                self._nodes.append(body_json_node)
                body_children = []
                for stmt in node.body:
                    body_children.append(self.traverse(stmt))
                body_json_node["children"] = body_children
        if isinstance(node, jtree.FormalParameter):
            json_node["value"] = node.name
            if node.type:
                children.append(self.traverse(node.type))
        if isinstance(node, jtree.BasicType):
            # append value to node
            json_node["value"] = node.name
        if isinstance(node, (jtree.LocalVariableDeclaration, jtree.ConstantDeclaration, jtree.FieldDeclaration)):
            for dec in node.declarators:
                children.append(self.traverse(dec))
            if node.type:
                children.append(self.traverse(node.type))
        if isinstance(node, jtree.VariableDeclarator):
            json_node["value"] = node.name
            if node.initializer:
                children.append(self.traverse(node.initializer))
        if isinstance(node, jtree.Literal):
            val = node.value
            if is_numeric(val):
                if is_int(val):
                    json_node["value"] = int(val)
                else:
                    json_node["value"] = float(val)
            else:
                json_node["value"] = node.value
        if isinstance(node, jtree.StatementExpression):
            if node.expression:
                children.append(self.traverse(node.expression))
        if isinstance(node, jtree.Assignment):
            if node.expressionl:
                children.append(self.traverse(node.expressionl))
            assignment_type_pos = len(self._nodes)
            children.append(assignment_type_pos)
            assignment_type_json_node = {"id": assignment_type_pos, "type": node.type}
            self._nodes.append(assignment_type_json_node)
            if node.value:
                children.append(self.traverse(node.value))
        if isinstance(node, (jtree.MemberReference, jtree.SuperMemberReference, jtree.This)):
            if node.postfix_operators:
                pass
            if node.prefix_operators:
                pass

            if node.member:
                json_node["value"] = node.member

            if node.qualifier:
                qual_pos = len(self._nodes)
                children.append(qual_pos)
                qualifier_json_node = {"id": qual_pos, "type": "qualifier", "value": node.qualifier}
                self._nodes.append(qualifier_json_node)

            if node.selectors:
                selectors_pos = len(self._nodes)
                children.append(selectors_pos)
                selectors_json_node = {"id": selectors_pos, "type": "selectors"}
                self._nodes.append(selectors_json_node)
                selectors_children = []
                for selector in node.selectors:
                    selectors_children.append(self.traverse(selector))
                selectors_json_node["children"] = selectors_children

        if isinstance(node, jtree.ForStatement):
            if node.control:
                children.append(self.traverse(node.control))
            if node.body:
                children.append(self.traverse(node.body))
        if isinstance(node, jtree.ForControl):
            if node.init:
                children.append(self.traverse(node.init))
            if node.condition:
                children.append(self.traverse(node.condition))
            if node.update:
                for stmt in node.update:
                    children.append(self.traverse(stmt))
        if isinstance(node, jtree.WhileStatement):
            if node.control:
                children.append(self.traverse(node.control))
            if node.body:
                children.append(self.traverse(node.body))
        if isinstance(node, jtree.DoStatement):
            if node.control:
                children.append(self.traverse(node.control))
            if node.body:
                children.append(self.traverse(node.body))
        if isinstance(node, jtree.IfStatement):
            if node.condition:
                children.append(self.traverse(node.condition))
            if node.then_statement:
                children.append(self.traverse(node.then_statement))
            if node.else_statement:
                children.append(self.traverse(node.else_statement))
        if isinstance(node, jtree.ReturnStatement):
            if node.expression:
                children.append(self.traverse(node.expression))
        if isinstance(node, jtree.BlockStatement):
            if node.statements:
                for stmt in node.statements:
                    children.append(self.traverse(stmt))
        if isinstance(node, jtree.ContinueStatement):
            # nothing to do
            pass
        if isinstance(node, jtree.BreakStatement):
            # nothing to do
            pass
        if isinstance(node, jtree.TryStatement):
            if node.block:
                block_pos = len(self._nodes)
                children.append(block_pos)
                block_json_node = {"id": block_pos, "type": "BlockStatement"}
                self._nodes.append(block_json_node)
                block_children = []
                for stmt in node.block:
                    block_children.append(self.traverse(stmt))
                block_json_node["children"] = block_children
            if node.catches:
                for catch in node.catches:
                    children.append(self.traverse(catch))
            if node.finally_block:
                finally_pos = len(self._nodes)
                children.append(finally_pos)
                finally_json_node = {"id": finally_pos, "type": "BlockStatement"}
                self._nodes.append(finally_json_node)
                finally_children = []
                for stmt in node.finally_block:
                    finally_children.append(self.traverse(stmt))
                finally_json_node["children"] = finally_children
        if isinstance(node, jtree.CatchClause):
            if node.parameter:
                children.append(self.traverse(node.parameter))
            if node.block:
                block_pos = len(self._nodes)
                children.append(block_pos)
                block_json_node = {"id": block_pos, "type": "BlockStatement"}
                self._nodes.append(block_json_node)
                block_children = []
                for stmt in node.block:
                    block_children.append(self.traverse(stmt))
                block_json_node["children"] = block_children
        if isinstance(node, jtree.CatchClauseParameter):
            # append value to node
            json_node["value"] = node.types[0]
        if isinstance(node, jtree.ThrowStatement):
            if node.expression:
                children.append(self.traverse(node.expression))
        if isinstance(node, jtree.EnhancedForControl):
            if node.iterable:
                children.append(self.traverse(node.iterable))
            if node.var:
                children.append(self.traverse(node.var))
        if isinstance(node, (jtree.MethodInvocation, jtree.SuperMethodInvocation, jtree.SuperConstructorInvocation, jtree.ExplicitConstructorInvocation)):
            if node.member:
                json_node["value"] = node.member
            if node.qualifier:
                qual_pos = len(self._nodes)
                children.append(qual_pos)
                qualifier_json_node = {"id": qual_pos, "type": "qualifier", "value": node.qualifier}
                self._nodes.append(qualifier_json_node)

            if node.arguments:
                arg_pos = len(self._nodes)
                children.append(arg_pos)
                arg_json_node = {"id": arg_pos, "type": "arguments"}
                self._nodes.append(arg_json_node)
                arg_children = []
                for arg in node.arguments:
                    arg_children.append(self.traverse(arg))
                arg_json_node["children"] = arg_children

            if node.selectors:
                selectors_pos = len(self._nodes)
                children.append(selectors_pos)
                selectors_json_node = {"id": selectors_pos, "type": "selectors"}
                self._nodes.append(selectors_json_node)
                selectors_children = []
                for selector in node.selectors:
                    selectors_children.append(self.traverse(selector))
                selectors_json_node["children"] = selectors_children
        if isinstance(node, jtree.LambdaExpression):
            if node.body:
                if isinstance(node.body, list):
                    body_pos = len(self._nodes)
                    children.append(body_pos)
                    body_json_node = {"id": body_pos, "type": "BlockStatement"}
                    self._nodes.append(body_json_node)
                    body_children = []
                    for stmt in node.body:
                        body_children.append(self.traverse(stmt))
                    body_json_node["children"] = body_children
                else:
                    children.append(self.traverse(node.body))
            if node.parameters:
                parameters_pos = len(self._nodes)
                children.append(parameters_pos)
                parameters_json_node = {"id": parameters_pos, "type": "parameters"}
                self._nodes.append(parameters_json_node)
                parameters_children = []
                for parameter in node.parameters:
                    parameters_children.append(self.traverse(parameter))
                parameters_json_node["children"] = parameters_children
        if isinstance(node, jtree.BinaryOperation):
            if node.operator:
                json_node["value"] = node.operator
            if node.operandl:
                children.append(self.traverse(node.operandl))
            if node.operandr:
                children.append(self.traverse(node.operandr))
        if isinstance(node, jtree.ReferenceType):
            json_node["value"] = node.name
            if node.arguments:
                arg_pos = len(self._nodes)
                children.append(arg_pos)
                arg_json_node = {"id": arg_pos, "type": "arguments"}
                self._nodes.append(arg_json_node)
                arg_children = []
                for arg in node.arguments:
                    arg_children.append(self.traverse(arg))
                arg_json_node["children"] = arg_children
        if isinstance(node, jtree.TypeArgument):
            if node.type:
                children.append(self.traverse(node.type))
        if isinstance(node, jtree.AssertStatement):
            if node.condition:
                children.append(self.traverse(node.condition))
            if node.value:
                children.append(self.traverse(node.value))
        if isinstance(node, jtree.TernaryExpression):
            if node.condition:
                children.append(self.traverse(node.condition))
            if node.if_true:
                children.append(self.traverse(node.if_true))
            if node.if_false:
                children.append(self.traverse(node.if_false))
        if isinstance(node, jtree.ArrayCreator):
            if node.qualifier:
                pass
            if node.dimensions:
                pass
            if node.initializer:
                children.append(self.traverse(node.initializer))
            if node.type:
                children.append(self.traverse(node.type))
            if node.selectors:
                pass
        if isinstance(node, jtree.ArraySelector):
            if node.index:
                children.append(self.traverse(node.index))
        if isinstance(node, jtree.ArrayInitializer):
            if node.initializers:
                for ini in node.initializers:
                    children.append(self.traverse(ini))
        if isinstance(node, jtree.SynchronizedStatement):
            if node.block:
                body_pos = len(self._nodes)
                children.append(body_pos)
                body_json_node = {"id": body_pos, "type": "BlockStatement"}
                self._nodes.append(body_json_node)
                body_children = []
                for stmt in node.block:
                    body_children.append(self.traverse(stmt))
                body_json_node["children"] = body_children
        if children:
            json_node["children"] = children
        return pos


if __name__ == '__main__':
    vv = parse_file("../bubble.java", False)
    print(vv)
