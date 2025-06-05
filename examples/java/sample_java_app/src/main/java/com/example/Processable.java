package com.example;

import java.util.List;
import java.util.Optional;

/**
 * Processable interface defines contract for data processing operations.
 * This interface demonstrates Java 21 features and various ontology elements.
 * 
 * @author Code Graph Example
 * @version 1.0
 * @since Java 21
 */
@FunctionalInterface
public interface Processable<T> {
    
    /**
     * Process data with given parameters
     * @param data the input data to process
     * @param config processing configuration
     * @return processed result wrapped in Optional
     * @throws ProcessingException if processing fails
     */
    Optional<T> process(T data, ProcessingConfig config) throws ProcessingException;
    
    /**
     * Default method for batch processing
     * @param dataList list of data items to process
     * @param config processing configuration
     * @return list of processed results
     */
    default List<Optional<T>> processBatch(List<T> dataList, ProcessingConfig config) {
        return dataList.stream()
                .map(data -> {
                    try {
                        return process(data, config);
                    } catch (ProcessingException e) {
                        System.err.println("Processing failed for item: " + data);
                        return Optional.empty();
                    }
                })
                .toList();
    }
    
    /**
     * Static utility method for validation
     * @param data data to validate
     * @return true if data is valid
     */
    static <T> boolean isValid(T data) {
        return data != null;
    }
}
