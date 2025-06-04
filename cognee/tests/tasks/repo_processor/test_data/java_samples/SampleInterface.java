package com.example.interfaces;

/**
 * Javadoc for SampleInterface.
 * This interface defines a contract for something.
 */
public interface SampleInterface {

    /**
     * Javadoc for performAction.
     * @param actionName The name of the action.
     * @param level The intensity level.
     */
    void performAction(String actionName, int level);

    /**
     * Javadoc for checkStatus.
     * @return True if status is okay, false otherwise.
     */
    boolean checkStatus();

    // A default method
    /**
     * Javadoc for defaultMethod.
     */
    default void defaultMethod() {
        System.out.println("Default implementation");
    }
}
