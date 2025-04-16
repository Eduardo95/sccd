import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

public class AstGenerator {
    private static Logger logger = LoggerFactory.getLogger(AstGenerator.class);
    private static ObjectMapper mapper = new ObjectMapper();

    private AstGenerator() {}
    public static Path input = Paths.get("/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/model_2level/atcoder_307_c/**.java");
    //public static Path output = null;
    public static Path output = Paths.get("/Users/eduardo/PycharmProjects/TwoLevelGenericASTProject/model_2level/atcoder_c/atcoder_java_fine");
    public static int maxNodes = 30000;
    public static int minNodes = 20;

    public static List<Map<String, Object>> parseFile(Path filepath, boolean methodOnly) throws IOException {
        Node result;
        if (methodOnly) {
            result = JavaParser.parseBodyDeclaration(new String(Files.readAllBytes(filepath)));
        } else {
            result = JavaParser.parse(filepath);
        }
        JsonVisitorFine visitor = new JsonVisitorFine();
        List<Map<String, Object>> astNodes = new ArrayList<>();
        result.accept(visitor, astNodes);
        return astNodes;
    }

    public static List<Map<String, Object>> parseFile(Path filepath) throws IOException {
        return parseFile(filepath, true);
    }

    public static void processFile(boolean methodOnly) throws IOException {
        List<Map<String, Object>> parsed = parseFile(input, methodOnly);
        String jsonAST = mapper.writeValueAsString(parsed);
        if (output == null) {
            System.out.println(jsonAST);
        } else {
            Files.write(output, jsonAST.getBytes(), StandardOpenOption.CREATE);
        }
    }

    public static void processAllFiles() throws IOException {

        FileFinder.Result filesResult = FileFinder.findFiles(input);

        Set<Path> files = filesResult.getFiles();

        int totalCount = files.size();
        logger.info("starting to process " + totalCount + " input");

        Path root = Paths.get("").toAbsolutePath();

        String jsonOutput = output.toString() + ".json";
        String filesOutput = output.toString() + ".txt";
        String failedOutput = output.toString() + "_failed.txt";

        final Object writeLock = new Object();

        try(PrintWriter jsonWriter = new PrintWriter(jsonOutput, "UTF-8");
            PrintWriter astWriter = new PrintWriter(filesOutput, "UTF-8");
            PrintWriter failedWriter = new PrintWriter(failedOutput, "UTF-8")) {

            AtomicInteger counter = new AtomicInteger(0);

            filesResult.getFiles().parallelStream().forEach(file -> {
                Path relativePath = root.relativize(file.toAbsolutePath());
                try {
                    List<Map<String, Object>> parsed = parseFile(file);

                    if (parsed.size() < minNodes) {
                        throw new RuntimeException("too few nodes");
                    }
                    if (parsed.size() > maxNodes) {
                        throw new RuntimeException("too many nodes");
                    }

                    String jsonAST = mapper.writeValueAsString(parsed);

                    synchronized(writeLock) {
                        jsonWriter.println(jsonAST);
                        astWriter.println(relativePath);
                    }

                    int currentCount = counter.getAndIncrement();
                    if (currentCount % 1000 == 0) {
                        logger.info("progress: " + currentCount + "/" + totalCount);
                    }
                } catch (Exception e) {
                    logger.debug("failed to parse " + file + ": " + e.getMessage());
                    failedWriter.println(relativePath + "\t" + e.getMessage());
                    //failedWriter.println(relativePath + "");
                }
            });
        }
    }

    public static void main(String[] args) {
        try {
            processAllFiles();
            //processFile(true);
        } catch (IOException e) {
            System.err.println("failed to process input file: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.err.println("failed to process input file: " + e.getMessage());
            System.exit(1);
        }
    }
}