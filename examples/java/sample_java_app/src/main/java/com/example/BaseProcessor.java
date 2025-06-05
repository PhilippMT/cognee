package com.example;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicLong;

/**
 * BaseProcessor provides common functionality for data processors.
 * Demonstrates abstract class, inheritance, generics, and composition.
 * 
 * @param <T> type of data this processor handles
 */
public abstract class BaseProcessor<T> implements Processable<T> {
    
    // Static field for tracking processor instances
    private static final AtomicLong instanceCounter = new AtomicLong(0);
    
    // Instance fields
    protected final String processorId;
    protected final String processorName;
    protected ProcessingStatus currentStatus;
    protected LocalDateTime createdAt;
    protected LocalDateTime lastProcessedAt;
    protected long processedCount;
    
    // Composition - processor has a configuration
    protected ProcessingConfig defaultConfig;
    
    /**
     * Protected constructor for BaseProcessor
     * @param processorName name of this processor
     */
    protected BaseProcessor(String processorName) {
        this.processorId = "PROC-" + instanceCounter.incrementAndGet();
        this.processorName = processorName;
        this.currentStatus = ProcessingStatus.PENDING;
        this.createdAt = LocalDateTime.now();
        this.processedCount = 0L;
        this.defaultConfig = new ProcessingConfig();
    }
    
    /**
     * Abstract method that subclasses must implement
     * @param data the data to process
     * @param config processing configuration
     * @return processed data
     */
    protected abstract T doProcess(T data, ProcessingConfig config) throws ProcessingException;
    
    /**
     * Template method pattern implementation
     */
    @Override
    public Optional<T> process(T data, ProcessingConfig config) {
        if (!isValid(data)) {
            return Optional.empty();
        }
        
        try {
            updateStatus(ProcessingStatus.IN_PROGRESS);
            T result = doProcess(data, config != null ? config : defaultConfig);
            updateStatus(ProcessingStatus.COMPLETED);
            incrementProcessedCount();
            return Optional.of(result);
        } catch (ProcessingException e) {
            updateStatus(ProcessingStatus.FAILED);
            throw new RuntimeException("Processing failed", e);
        }
    }
    
    /**
     * Asynchronous processing method
     * @param data data to process
     * @param config processing configuration
     * @return CompletableFuture with result
     */
    public CompletableFuture<Optional<T>> processAsync(T data, ProcessingConfig config) {
        return CompletableFuture.supplyAsync(() -> process(data, config));
    }
    
    /**
     * Update processor status
     * @param newStatus the new status
     */
    protected synchronized void updateStatus(ProcessingStatus newStatus) {
        this.currentStatus = newStatus;
        this.lastProcessedAt = LocalDateTime.now();
    }
    
    /**
     * Increment processed count atomically
     */
    protected synchronized void incrementProcessedCount() {
        this.processedCount++;
    }
    
    // Getter methods
    public String getProcessorId() { return processorId; }
    public String getProcessorName() { return processorName; }
    public ProcessingStatus getCurrentStatus() { return currentStatus; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getLastProcessedAt() { return lastProcessedAt; }
    public long getProcessedCount() { return processedCount; }
    
    /**
     * Get processor statistics
     * @return formatted statistics string
     */
    public String getStatistics() {
        return String.format(
            "Processor[id=%s, name=%s, status=%s, processed=%d, created=%s]",
            processorId, processorName, currentStatus, processedCount, createdAt
        );
    }
    
    /**
     * Static factory method
     * @param type processor type
     * @return processor instance based on type
     */
    public static BaseProcessor<String> createProcessor(String type) {
        switch (type.toLowerCase()) {
            case "text":
                return new TextProcessor();
            case "data":
                return new DataProcessor();
            default:
                throw new IllegalArgumentException("Unknown processor type: " + type);
        }
    }
}
