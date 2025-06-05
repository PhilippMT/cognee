package com.example;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * ProcessingApplication demonstrates a complete Java application
 * with various design patterns and language features.
 * 
 * This class serves as the main entry point and orchestrator.
 */
public class ProcessingApplication {
    
    private final TextProcessor textProcessor;
    private final DataProcessor dataProcessor;
    private final ProcessingConfig globalConfig;
    
    /**
     * Constructor initializes the application
     */
    public ProcessingApplication() {
        this.textProcessor = new TextProcessor(true, false, false);
        this.dataProcessor = new DataProcessor();
        this.globalConfig = new ProcessingConfig();
        
        // Configure global settings
        globalConfig.enable("word_count");
        globalConfig.enable("statistics");
    }
    
    /**
     * Main method - application entry point
     * @param args command line arguments
     */
    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println("Java Code Graph Example Application");
        System.out.println("============================================================");
        
        ProcessingApplication app = new ProcessingApplication();
        app.runDemo();
        
        System.out.println("============================================================");
        System.out.println("Application completed successfully!");
        System.out.println("============================================================");
    }
    
    /**
     * Run the application demo
     */
    public void runDemo() {
        try {
            demonstrateTextProcessing();
            demonstrateDataProcessing();
            demonstrateAsyncProcessing();
            demonstrateBatchProcessing();
            demonstrateErrorHandling();
            printStatistics();
        } catch (Exception e) {
            System.err.println("Demo failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Demonstrate text processing capabilities
     */
    private void demonstrateTextProcessing() {
        System.out.println("\n--- Text Processing Demo ---");
        
        String[] testTexts = {
            "Hello, World! This is a test.",
            "   Extra   whitespace   text   ",
            "Text with MIXED case Letters",
            "Special @#$% Characters &*() Text"
        };
        
        for (String text : testTexts) {
            Optional<String> result = textProcessor.process(text, globalConfig);
            result.ifPresent(processed -> 
                System.out.printf("Original: '%s' -> Processed: '%s'%n", text, processed)
            );
        }
        
        // Demonstrate additional text methods
        String sample = "The quick brown fox jumps over the lazy dog";
        System.out.println("\nAdditional Text Operations:");
        System.out.println("Reversed words: " + textProcessor.reverseWords(sample));
        System.out.println("Contains 'fox': " + textProcessor.containsKeywords(sample, "fox", "cat"));
        System.out.println("Sentences: " + String.join(" | ", textProcessor.splitIntoSentences(sample + ".")));
    }
    
    /**
     * Demonstrate data processing capabilities
     */
    private void demonstrateDataProcessing() {
        System.out.println("\n--- Data Processing Demo ---");
        
        String[] testData = {
            "data_item_1",
            "data_item_2",
            "data_item_3"
        };
        
        for (String data : testData) {
            Optional<String> result = dataProcessor.process(data, globalConfig);
            result.ifPresent(processed -> 
                System.out.printf("Data: '%s' -> Processed: '%s'%n", data, processed)
            );
        }
    }
    
    /**
     * Demonstrate asynchronous processing
     */
    private void demonstrateAsyncProcessing() {
        System.out.println("\n--- Async Processing Demo ---");
        
        try {
            CompletableFuture<Optional<String>> future1 = 
                textProcessor.processAsync("Async text 1", globalConfig);
            CompletableFuture<Optional<String>> future2 = 
                textProcessor.processAsync("Async text 2", globalConfig);
            
            // Wait for both to complete
            CompletableFuture.allOf(future1, future2).get();
            
            System.out.println("Async result 1: " + future1.get().orElse("Failed"));
            System.out.println("Async result 2: " + future2.get().orElse("Failed"));
            
        } catch (InterruptedException | ExecutionException e) {
            System.err.println("Async processing failed: " + e.getMessage());
        }
    }
    
    /**
     * Demonstrate batch processing
     */
    private void demonstrateBatchProcessing() {
        System.out.println("\n--- Batch Processing Demo ---");
        
        List<String> batchData = List.of(
            "Batch item 1",
            "Batch item 2", 
            "Batch item 3",
            null,  // This should be handled gracefully
            "Batch item 5"
        );
        
        List<Optional<String>> results = textProcessor.processBatch(batchData, globalConfig);
        
        for (int i = 0; i < batchData.size(); i++) {
            String original = batchData.get(i);
            String processed = results.get(i).orElse("FAILED");
            System.out.printf("Batch[%d]: '%s' -> '%s'%n", i, original, processed);
        }
    }
    
    /**
     * Demonstrate error handling
     */
    private void demonstrateErrorHandling() {
        System.out.println("\n--- Error Handling Demo ---");
        
        // Test with null and empty data
        try {
            textProcessor.process(null, globalConfig);
        } catch (Exception e) {
            System.out.println("Handled null input: " + e.getMessage());
        }
        
        try {
            textProcessor.process("", globalConfig);
        } catch (Exception e) {
            System.out.println("Handled empty input: " + e.getMessage());
        }
        
        // Demonstrate status transitions
        System.out.println("\nStatus Transitions:");
        for (ProcessingStatus status : ProcessingStatus.values()) {
            System.out.printf("Status: %s, Terminal: %s, Successful: %s%n", 
                status, status.isTerminal(), status.isSuccessful());
        }
    }
    
    /**
     * Print processing statistics
     */
    private void printStatistics() {
        System.out.println("\n--- Processing Statistics ---");
        System.out.println("Text Processor: " + textProcessor.getStatistics());
        System.out.println("Data Processor: " + dataProcessor.getStatistics());
        
        System.out.println("\nProcessor Details:");
        System.out.println(textProcessor.toString());
        System.out.println(dataProcessor.toString());
    }
}

/**
 * Supporting classes for the application
 */

/**
 * Custom exception for processing errors
 */
class ProcessingException extends Exception {
    public ProcessingException(String message) {
        super(message);
    }
    
    public ProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}

/**
 * Configuration class for processing parameters
 */
class ProcessingConfig {
    private final Map<String, Boolean> settings = new java.util.HashMap<>();
    
    public void enable(String setting) {
        settings.put(setting, true);
    }
    
    public void disable(String setting) {
        settings.put(setting, false);
    }
    
    public boolean isEnabled(String setting) {
        return settings.getOrDefault(setting, false);
    }
    
    public Map<String, Boolean> getAllSettings() {
        return new java.util.HashMap<>(settings);
    }
}

/**
 * Another concrete processor implementation
 */
class DataProcessor extends BaseProcessor<String> {
    
    public DataProcessor() {
        super("DataProcessor");
    }
    
    @Override
    protected String doProcess(String data, ProcessingConfig config) throws ProcessingException {
        if (data == null) {
            throw new ProcessingException("Data cannot be null");
        }
        
        // Simple data processing simulation
        String processed = "PROCESSED[" + data.toUpperCase() + "]";
        
        if (config.isEnabled("statistics")) {
            processed += "_STATS[len=" + data.length() + "]";
        }
        
        return processed;
    }
}
