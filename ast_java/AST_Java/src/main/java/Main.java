import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.Node;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Main{
    private static Logger logger = LoggerFactory.getLogger(AstGenerator.class);
    private static ObjectMapper mapper = new ObjectMapper();

    private Main() {}
    public static Path input = Paths.get("/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/ast_java/bubble.java");

    public static int maxNodes = 30000;
    public static int minNodes = 20;

    public static List<Map<String, Object>> parseFile(Path filepath, boolean methodOnly) throws IOException {
        Node result;
        if (methodOnly) {
            result = JavaParser.parseBodyDeclaration(new String(Files.readAllBytes(filepath)));
        } else {
            result = JavaParser.parse(filepath);
        }
        JsonVisitorCoarse visitor = new JsonVisitorCoarse();
        List<Map<String, Object>> astNodes = new ArrayList<>();
        result.accept(visitor, astNodes);
        return astNodes;
    }

    public static List<Map<String, Object>> parseFile(Path filepath) throws IOException {
        return parseFile(filepath, false);
    }

    public static void processFile(boolean methodOnly) throws IOException {
        List<Map<String, Object>> parsed = parseFile(input, methodOnly);
        String jsonAST = mapper.writeValueAsString(parsed);

        System.out.println(jsonAST);

    }
    public static void main(String[] args){
        try {
            processFile(false);
        } catch (IOException e) {
            System.err.println("failed to process input file: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.err.println("failed to process input file: " + e.getMessage());
            System.exit(1);
        }
    }
}
