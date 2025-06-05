package com.example;

import java.util.Arrays;
import java.util.regex.Pattern;

/**
 * TextProcessor handles text-specific processing operations.
 * Demonstrates concrete class implementation, method overriding, and annotations.
 */
@SuppressWarnings("unused")
public class TextProcessor extends BaseProcessor<String> {
    
    // Regular expression patterns for text processing
    private static final Pattern WHITESPACE_PATTERN = Pattern.compile("\\s+");
    private static final Pattern SPECIAL_CHARS_PATTERN = Pattern.compile("[^a-zA-Z0-9\\s]");
    
    // Configuration fields
    private boolean trimWhitespace = true;
    private boolean removeSpecialChars = false;
    private boolean convertToLowerCase = false;
    
    /**
     * Constructor for TextProcessor
     */
    public TextProcessor() {
        super("TextProcessor");
    }
    
    /**
     * Constructor with configuration
     * @param trimWhitespace whether to trim whitespace
     * @param removeSpecialChars whether to remove special characters
     * @param convertToLowerCase whether to convert to lowercase
     */
    public TextProcessor(boolean trimWhitespace, boolean removeSpecialChars, boolean convertToLowerCase) {
        super("ConfiguredTextProcessor");
        this.trimWhitespace = trimWhitespace;
        this.removeSpecialChars = removeSpecialChars;
        this.convertToLowerCase = convertToLowerCase;
    }
    
    /**
     * Implementation of abstract method from BaseProcessor
     * @param text the text to process
     * @param config processing configuration
     * @return processed text
     * @throws ProcessingException if processing fails
     */
    @Override
    protected String doProcess(String text, ProcessingConfig config) throws ProcessingException {
        if (text == null || text.isEmpty()) {
            throw new ProcessingException("Text cannot be null or empty");
        }
        
        String result = text;
        
        // Apply text transformations based on configuration
        if (trimWhitespace) {
            result = normalizeWhitespace(result);
        }
        
        if (removeSpecialChars) {
            result = removeSpecialCharacters(result);
        }
        
        if (convertToLowerCase) {
            result = result.toLowerCase();
        }
        
        // Apply config-specific transformations
        if (config.isEnabled("uppercase")) {
            result = result.toUpperCase();
        }
        
        if (config.isEnabled("word_count")) {
            int wordCount = countWords(result);
            result = result + " [Words: " + wordCount + "]";
        }
        
        return result;
    }
    
    /**
     * Normalize whitespace in text
     * @param text input text
     * @return text with normalized whitespace
     */
    private String normalizeWhitespace(String text) {
        return WHITESPACE_PATTERN.matcher(text.trim()).replaceAll(" ");
    }
    
    /**
     * Remove special characters from text
     * @param text input text
     * @return text without special characters
     */
    private String removeSpecialCharacters(String text) {
        return SPECIAL_CHARS_PATTERN.matcher(text).replaceAll("");
    }
    
    /**
     * Count words in text
     * @param text input text
     * @return number of words
     */
    private int countWords(String text) {
        if (text == null || text.trim().isEmpty()) {
            return 0;
        }
        return text.trim().split("\\s+").length;
    }
    
    /**
     * Split text into sentences
     * @param text input text
     * @return array of sentences
     */
    public String[] splitIntoSentences(String text) {
        if (text == null || text.trim().isEmpty()) {
            return new String[0];
        }
        return text.split("[.!?]+");
    }
    
    /**
     * Reverse the order of words in text
     * @param text input text
     * @return text with reversed word order
     */
    public String reverseWords(String text) {
        if (text == null || text.trim().isEmpty()) {
            return text;
        }
        
        String[] words = text.trim().split("\\s+");
        StringBuilder reversed = new StringBuilder();
        
        for (int i = words.length - 1; i >= 0; i--) {
            reversed.append(words[i]);
            if (i > 0) {
                reversed.append(" ");
            }
        }
        
        return reversed.toString();
    }
    
    /**
     * Check if text contains any of the specified keywords
     * @param text text to search
     * @param keywords keywords to search for
     * @return true if any keyword is found
     */
    public boolean containsKeywords(String text, String... keywords) {
        if (text == null || keywords == null) {
            return false;
        }
        
        String lowerText = text.toLowerCase();
        return Arrays.stream(keywords)
                .anyMatch(keyword -> lowerText.contains(keyword.toLowerCase()));
    }
    
    // Setter methods for configuration
    public void setTrimWhitespace(boolean trimWhitespace) {
        this.trimWhitespace = trimWhitespace;
    }
    
    public void setRemoveSpecialChars(boolean removeSpecialChars) {
        this.removeSpecialChars = removeSpecialChars;
    }
    
    public void setConvertToLowerCase(boolean convertToLowerCase) {
        this.convertToLowerCase = convertToLowerCase;
    }
    
    @Override
    public String toString() {
        return String.format("TextProcessor[id=%s, trimWhitespace=%s, removeSpecialChars=%s, convertToLowerCase=%s]",
                getProcessorId(), trimWhitespace, removeSpecialChars, convertToLowerCase);
    }
}
