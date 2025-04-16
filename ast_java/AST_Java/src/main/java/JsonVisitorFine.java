import com.github.javaparser.ast.*;
import com.github.javaparser.ast.body.*;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.JavadocComment;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.*;
import com.github.javaparser.ast.type.*;
import com.github.javaparser.ast.visitor.GenericVisitorAdapter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * This class implements a Visitor which visits the AST and
 * returns a serializable object
 */
public class JsonVisitorFine extends GenericVisitorAdapter<Integer, List<Map<String, Object>>> {
    public static String idKey = "id";
    public static String typeKey = "type";
    public static String valueKey = "value";
    public static String childrenKey = "children";
    public static String modifiersKey = "modifiers";

    private Map<String, Object> enterNode(Node node, List<Map<String, Object>> nodes) {
        Map<String, Object> result = new HashMap<>();
        result.put(idKey, nodes.size());
        result.put(typeKey, node.getClass().getSimpleName());
        nodes.add(result);
        return result;
    }

    private Map<String, Object> enterNode(String nodename, List<Map<String, Object>> nodes) {
        Map<String, Object> result = new HashMap<>();
        result.put(idKey, nodes.size());
        result.put(typeKey, nodename);
        nodes.add(result);
        return result;
    }

    private List<Integer> addChildren(Map<String, Object> result) {
        List<Integer> children = new ArrayList<>();
        result.put(childrenKey, children);
        return children;
    }

    private String getBinaryOperator(String operator){
        if(operator.equals("&&")){
            return "and";
        }else if (operator.equals("||")){
            return "or";
        }else if (operator.equals("+")){
            return "add";
        }else if (operator.equals("-")){
            return "sub";
        }else if (operator.equals("*")){
            return "multiply";
        }else if (operator.equals("/")){
            return "divide";
        }else if (operator.equals("<<")){
            return "lshift";
        }else if (operator.equals(">>")){
            return "rshift";
        }else if (operator.equals("|")){
            return "bitor";
        }else if (operator.equals("^")){
            return "bitxor";
        }else if (operator.equals("&")){
            return "bitand";
        }else if (operator.equals("==")){
            return "equal";
        }else if (operator.equals("!=")){
            return "notequal";
        }else if (operator.equals("<")){
            return "lt";
        }else if (operator.equals("<=")){
            return "lte";
        }else if (operator.equals(">")){
            return "gt";
        }else if (operator.equals(">=")){
            return "gte";
        }else if (operator.equals(">>>")){
            return "unsignedrshift";
        }else if (operator.equals("%")){
            return "remainder";
        }
        return "";
    }

    private String getUnaryOperator(String operator){
        if(operator.equals("~")){
            return "invert";
        }else if(operator.equals("!")){
            return "not";
        }else if(operator.equals("+")){
            return "uadd";
        }else if(operator.equals("-")){
            return "usub";
        }else if(operator.equals("++")){
            return "increment";
        }else if(operator.equals("--")){
            return "decrement";
        }
        return "";
    }

    public Integer visit(NodeList n, List<Map<String, Object>> arg) {
        throw new RuntimeException("NodeList visit should not be called, use foreach instead");
    }

    public Integer visit(AnnotationDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        n.getMembers().forEach(m -> children.add(m.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(AnnotationMemberDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(modifiersKey, n.getModifiers().toString());
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        children.add(n.getType().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ArrayAccessExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "arrayaccess");
        List<Integer> children = addChildren(result);
        children.add(n.getIndex().accept(this, arg));
        children.add(n.getName().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ArrayCreationExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "arraydec");
        List<Integer> children = addChildren(result);
        children.add(n.getElementType().accept(this, arg));
        n.getInitializer().ifPresent( c -> children.add(c.accept(this, arg)));
        //n.getLevels().forEach(l -> children.add(l.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ArrayCreationLevel n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        n.getDimension().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ArrayInitializerExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "ListLoad");
        List<Integer> children = addChildren(result);
        n.getValues().forEach(v -> children.add(v.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ArrayType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        List<Integer> children = addChildren(result);
        children.add(n.getComponentType().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(AssertStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "assert");
        List<Integer> children = addChildren(result);
        children.add(n.getCheck().accept(this, arg));
        n.getMessage().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(AssignExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "assignment");
        List<Integer> children = addChildren(result);
        children.add(n.getTarget().accept(this, arg));
        children.add(n.getValue().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(BinaryExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, getBinaryOperator(n.getOperator().asString()));
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getOperator().asString());
        children.add(n.getLeft().accept(this, arg));
        children.add(n.getRight().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(BlockComment n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(valueKey, n.getContent());
        return (Integer)result.get(idKey);
    }

    public Integer visit(BlockStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "block");
        List<Integer> children = addChildren(result);
        n.getStatements().forEach(stmt -> children.add(stmt.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(BooleanLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        result.put(valueKey, String.valueOf(n.getValue()));
        return (Integer)result.get(idKey);
    }

    public Integer visit(BreakStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "break");
        return (Integer)result.get(idKey);
    }

    public Integer visit(CastExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "cast");
        List<Integer> children = addChildren(result);
        children.add(n.getExpression().accept(this, arg));
        children.add(n.getType().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(CatchClause n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "catch");
        List<Integer> children = addChildren(result);
        children.add(n.getBody().accept(this, arg));
        //children.add(n.getParameter().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(CharLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        result.put(valueKey, n.getValue());
        return (Integer)result.get(idKey);
    }

    public Integer visit(ClassExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "expression");
        List<Integer> children = addChildren(result);
        children.add(n.getType().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ClassOrInterfaceDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "classdef");
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        //n.getExtendedTypes().forEach(t -> children.add(t.accept(this, arg)));
        //n.getImplementedTypes().forEach(t -> children.add(t.accept(this, arg)));
        Map<String, Object> block = enterNode("block", arg);
        List<Integer> blockChildren = addChildren(block);
        n.getMembers().forEach(m -> blockChildren.add(m.accept(this, arg)));
        children.add((Integer)block.get(idKey));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ClassOrInterfaceType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        n.getTypeArguments().ifPresent( ts -> ts.forEach( t -> children.add(t.accept(this, arg))));
        return (Integer)result.get(idKey);
    }

    public Integer visit(CompilationUnit n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "root");
        List<Integer> children = addChildren(result);
        n.getImports().forEach(imp -> children.add(imp.accept(this, arg)));
        n.getTypes().forEach(t -> children.add(t.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ConditionalExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "ternary");
        List<Integer> children = addChildren(result);
        children.add(n.getCondition().accept(this, arg));
        children.add(n.getThenExpr().accept(this, arg));
        children.add(n.getElseExpr().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ConstructorDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "funcdef");
        List<Integer> children = addChildren(result);
        result.put(modifiersKey, n.getModifiers().toString());
        children.add(n.getBody().accept(this, arg));
        result.put(valueKey, n.getName().getIdentifier());

        Map<String, Object> param = enterNode("param", arg);
        Map<String, Object> typeParam = enterNode("typeparam", arg);

        List<Integer> paramChildren = addChildren(param);
        List<Integer> typeParamChildren = addChildren(typeParam);

        for (TypeParameter tp:n.getTypeParameters()){
            Integer id = tp.accept(this, arg);
            typeParamChildren.add(id);
        }
        for (Parameter p:n.getParameters()){
            Integer id = p.accept(this, arg);
            paramChildren.add(id);
        }
        children.add((Integer)param.get(idKey));
        n.getThrownExceptions().forEach(e -> children.add(e.accept(this, arg)));
        children.add((Integer)typeParam.get(idKey));
        //n.getParameters().forEach(p -> children.add(p.accept(this, arg)));
        //n.getTypeParameters().forEach(t -> children.add(t.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ContinueStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "continue");
        return (Integer)result.get(idKey);
    }

    public Integer visit(DoStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "dowhile");
        List<Integer> children = addChildren(result);
        children.add(n.getCondition().accept(this, arg));
        children.add(n.getBody().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(DoubleLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        result.put(valueKey, n.getValue());
        return (Integer)result.get(idKey);
    }

    public Integer visit(EmptyStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "empty");
        return (Integer)result.get(idKey);
    }

    public Integer visit(EnclosedExpr n, List<Map<String, Object>> arg) {
        int id = n.getInner().accept(this, arg);
        return id;
//        Map<String, Object> result = enterNode(n, arg);
//        result.put(typeKey, "expression");
//        List<Integer> children = addChildren(result);
//        children.add(n.getInner().accept(this, arg));
//        return (Integer)result.get(idKey);
    }

    public Integer visit(EnumConstantDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        n.getArguments().forEach(a -> children.add(a.accept(this, arg)));
        n.getClassBody().forEach(b -> children.add(b.accept(this, arg)));
        result.put(valueKey, n.getName().getIdentifier());
        return (Integer)result.get(idKey);
    }

    public Integer visit(EnumDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        n.getEntries().forEach(e -> children.add(e.accept(this, arg)));
        n.getImplementedTypes().forEach(t -> children.add(t.accept(this, arg)));
        n.getMembers().forEach(m -> children.add(m.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ExplicitConstructorInvocationStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "call");
        List<Integer> children = addChildren(result);
        result.put("isThis", n.isThis());
        n.getArguments().forEach(a -> children.add(a.accept(this, arg)));
        n.getExpression().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ExpressionStmt n, List<Map<String, Object>> arg) {
        int id = n.getExpression().accept(this, arg);
        return id;

//        Map<String, Object> result = enterNode(n, arg);
//        result.put(typeKey, "expression");
//        List<Integer> children = addChildren(result);
//        children.add(n.getExpression().accept(this, arg));
//        return (Integer)result.get(idKey);
    }

    public Integer visit(FieldAccessExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "AttributeLoad");
        List<Integer> children = addChildren(result);
        children.add(n.getScope().accept(this, arg));
        result.put(valueKey, n.getName().getIdentifier());
        return (Integer)result.get(idKey);
    }

    public Integer visit(FieldDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        result.put(typeKey, "vardec");
//        int length = n.getVariables().size();
//        if (length != 1){
//        System.out.println(length);}
        n.getVariables().forEach(v -> children.add(v.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ForStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "for");
        List<Integer> children = addChildren(result);
        n.getInitialization().forEach(i -> children.add(i.accept(this, arg)));
        n.getCompare().ifPresent( c -> children.add(c.accept(this, arg)));
        n.getUpdate().forEach(u -> children.add(u.accept(this, arg)));
        children.add(n.getBody().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ForeachStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "foreach");
        List<Integer> children = addChildren(result);
        children.add(n.getBody().accept(this, arg));
        children.add(n.getIterable().accept(this, arg));
        children.add(n.getVariable().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(IfStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "if");
        List<Integer> children = addChildren(result);
        children.add(n.getCondition().accept(this, arg));
        children.add(n.getThenStmt().accept(this, arg));
        n.getElseStmt().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ImportDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "import");
        return (Integer)result.get(idKey);
    }

    public Integer visit(InitializerDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        result.put("isStatic", n.isStatic());
        children.add(n.getBody().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(InstanceOfExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getType().accept(this, arg));
        children.add(n.getExpression().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(IntegerLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        result.put(valueKey, n.getValue());
        return (Integer)result.get(idKey);
    }

    public Integer visit(IntersectionType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        List<Integer> children = addChildren(result);
        n.getElements().forEach(e -> children.add(e.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(JavadocComment n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(valueKey, n.getContent());
        return (Integer)result.get(idKey);
    }

    public Integer visit(LabeledStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getLabel().accept(this, arg));
        children.add(n.getStatement().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(LambdaExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "lambda");
        List<Integer> children = addChildren(result);

        Map<String, Object> param = enterNode("param", arg);
        List<Integer> paramChildren = addChildren(param);
        for (Parameter p:n.getParameters()){
            Integer id = p.accept(this, arg);
            paramChildren.add(id);
        }
        children.add((Integer)param.get(idKey));

        //n.getParameters().forEach(p -> children.add(p.accept(this, arg)));
        children.add(n.getBody().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(LineComment n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(valueKey, n.getContent());
        return (Integer)result.get(idKey);
    }

    public Integer visit(LocalClassDeclarationStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getClassDeclaration().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(LongLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        result.put(valueKey, n.getValue());
        return (Integer)result.get(idKey);
    }

    public Integer visit(MarkerAnnotationExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getName().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(MemberValuePair n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        children.add(n.getValue().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(MethodCallExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "call");
        List<Integer> children = addChildren(result);
        n.getScope().ifPresent( c -> children.add(c.accept(this, arg)));
        result.put(valueKey, n.getName().getIdentifier());
        n.getArguments().forEach(a -> children.add(a.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(MethodDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "funcdef");
        List<Integer> children = addChildren(result);
        children.add(n.getType().accept(this, arg));
        result.put(valueKey, n.getName().getIdentifier());


        Map<String, Object> param = enterNode("param", arg);
        Map<String, Object> typeParam = enterNode("typeparam", arg);

        List<Integer> paramChildren = addChildren(param);
        List<Integer> typeParamChildren = addChildren(typeParam);

        for (TypeParameter tp:n.getTypeParameters()){
            Integer id = tp.accept(this, arg);
            typeParamChildren.add(id);
        }
        for (Parameter p:n.getParameters()){
            Integer id = p.accept(this, arg);
            paramChildren.add(id);
        }
        children.add((Integer)param.get(idKey));
        children.add((Integer)typeParam.get(idKey));

        //n.getTypeParameters().forEach(t -> children.add(t.accept(this, arg)));
        //n.getParameters().forEach(p -> children.add(p.accept(this, arg)));
        n.getThrownExceptions().forEach(e -> children.add(e.accept(this, arg)));
        n.getBody().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(MethodReferenceExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        // TODO
        List<Integer> children = addChildren(result);
        children.add(n.getScope().accept(this, arg));
        result.put("identifier", n.getIdentifier());
        return (Integer)result.get(idKey);
    }

    public Integer visit(NameExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "identifier");
        result.put(valueKey, n.getName().getIdentifier());
        return (Integer)result.get(idKey);
    }

    public Integer visit(Name n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "identifier");
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getIdentifier());
        n.getQualifier().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(NormalAnnotationExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getName().accept(this, arg));
        n.getPairs().forEach(p -> children.add(p.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(NullLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        return (Integer)result.get(idKey);
    }

    public Integer visit(ObjectCreationExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "call");
        List<Integer> children = addChildren(result);
        n.getAnonymousClassBody().ifPresent( cb -> cb.forEach(c -> children.add(c.accept(this, arg))));
        n.getArguments().forEach(a -> children.add(a.accept(this, arg)));
        children.add(n.getType().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(PackageDeclaration n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getName().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(Parameter n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "arg");
        List<Integer> children = addChildren(result);
        children.add(n.getType().accept(this, arg));
        result.put(valueKey, n.getName().getIdentifier());
        return (Integer)result.get(idKey);
    }

    public Integer visit(PrimitiveType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        result.put(valueKey, n.getType().asString());
        return (Integer)result.get(idKey);
    }

    public Integer visit(ReturnStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "return");
        List<Integer> children = addChildren(result);
        n.getExpression().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(SimpleName n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "identifier");
        result.put(valueKey, n.getIdentifier());
        return (Integer)result.get(idKey);
    }

    public Integer visit(SingleMemberAnnotationExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getMemberValue().accept(this, arg));
        children.add(n.getName().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(StringLiteralExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "constant");
        result.put(valueKey, n.getValue());
        return (Integer)result.get(idKey);
    }

    public Integer visit(SuperExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        n.getClassExpr().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(SwitchEntryStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "case");
        List<Integer> children = addChildren(result);
        n.getStatements().forEach(s -> children.add(s.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(SwitchStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "switch");
        List<Integer> children = addChildren(result);
        children.add(n.getSelector().accept(this, arg));
        n.getEntries().forEach(e -> children.add(e.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(SynchronizedStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        children.add(n.getExpression().accept(this, arg));
        children.add(n.getBody().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ThisExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        List<Integer> children = addChildren(result);
        n.getClassExpr().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(ThrowStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "throw");
        List<Integer> children = addChildren(result);
        children.add(n.getExpression().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(TryStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "try");
        List<Integer> children = addChildren(result);
        //n.getResources().forEach(r -> children.add(r.accept(this, arg)));
        children.add(n.getTryBlock().accept(this, arg));
        n.getCatchClauses().forEach(c -> children.add(c.accept(this, arg)));
        n.getFinallyBlock().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(TypeExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "expression");
        List<Integer> children = addChildren(result);
        children.add(n.getType().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(TypeParameter n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "typearg");
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getName().getIdentifier());
        //n.getTypeBound().forEach(t -> children.add(t.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(UnaryExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, getUnaryOperator(n.getOperator().asString()));
        List<Integer> children = addChildren(result);
        result.put(valueKey, n.getOperator().asString());
        children.add(n.getExpression().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(UnionType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        List<Integer> children = addChildren(result);
        n.getElements().forEach(e -> children.add(e.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(UnknownType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        return (Integer)result.get(idKey);
    }

    public Integer visit(VariableDeclarationExpr n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "vardec");
        List<Integer> children = addChildren(result);
        n.getVariables().forEach(v -> children.add(v.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(VariableDeclarator n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "var");
        List<Integer> children = addChildren(result);
        children.add(n.getType().accept(this, arg));
        result.put(valueKey, n.getName().getIdentifier());
        n.getInitializer().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }

    public Integer visit(VoidType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        return (Integer)result.get(idKey);
    }

    public Integer visit(WhileStmt n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "while");
        List<Integer> children = addChildren(result);
        children.add(n.getCondition().accept(this, arg));
        children.add(n.getBody().accept(this, arg));
        return (Integer)result.get(idKey);
    }

    public Integer visit(WildcardType n, List<Map<String, Object>> arg) {
        Map<String, Object> result = enterNode(n, arg);
        result.put(typeKey, "type");
        List<Integer> children = addChildren(result);
        n.getExtendedType().ifPresent( c -> children.add(c.accept(this, arg)));
        n.getSuperType().ifPresent( c -> children.add(c.accept(this, arg)));
        return (Integer)result.get(idKey);
    }
}
