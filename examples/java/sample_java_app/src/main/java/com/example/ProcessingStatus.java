package com.example;

/**
 * ProcessingStatus enum represents different states of data processing.
 * Demonstrates enum with fields, constructors, and methods.
 */
public enum ProcessingStatus {
    PENDING("Processing is pending", 0),
    IN_PROGRESS("Currently processing", 1),
    COMPLETED("Processing completed successfully", 2),
    FAILED("Processing failed", -1),
    CANCELLED("Processing was cancelled", -2);
    
    private final String description;
    private final int priority;
    
    /**
     * Constructor for ProcessingStatus enum
     * @param description human-readable description
     * @param priority processing priority level
     */
    ProcessingStatus(String description, int priority) {
        this.description = description;
        this.priority = priority;
    }
    
    /**
     * Get the description of this status
     * @return status description
     */
    public String getDescription() {
        return description;
    }
    
    /**
     * Get the priority of this status
     * @return priority level
     */
    public int getPriority() {
        return priority;
    }
    
    /**
     * Check if this status indicates completion
     * @return true if processing is done (either success or failure)
     */
    public boolean isTerminal() {
        return this == COMPLETED || this == FAILED || this == CANCELLED;
    }
    
    /**
     * Check if this status indicates success
     * @return true if processing completed successfully
     */
    public boolean isSuccessful() {
        return this == COMPLETED;
    }
    
    /**
     * Get status by priority level
     * @param priority the priority to search for
     * @return matching ProcessingStatus or null
     */
    public static ProcessingStatus getByPriority(int priority) {
        for (ProcessingStatus status : values()) {
            if (status.priority == priority) {
                return status;
            }
        }
        return null;
    }
    
    @Override
    public String toString() {
        return String.format("%s: %s (Priority: %d)", name(), description, priority);
    }
}
