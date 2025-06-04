package com.example.simple;

/**
 * This is a Javadoc for SampleClass.
 * It demonstrates basic class structure.
 */
public class SampleClass {

    /**
     * Javadoc for stringField.
     */
    private String stringField;

    /**
     * Javadoc for intField.
     */
    protected int intField = 42;

    // No Javadoc for this field
    double doubleField;

    /**
     * Constructor Javadoc.
     * @param initialStringValue The initial value for stringField.
     */
    public SampleClass(String initialStringValue) {
        this.stringField = initialStringValue;
    }

    /**
     * Javadoc for getStringField.
     * @return The current value of stringField.
     */
    public String getStringField() {
        return stringField;
    }

    /**
     * Javadoc for setStringField.
     * @param stringField The new value for stringField.
     */
    public void setStringField(String stringField) {
        this.stringField = stringField;
    }

    /**
     * Javadoc for processData.
     * @param count The number of times to process.
     * @param data The data to process.
     * @return A processed string.
     * @throws IllegalArgumentException if count is negative.
     */
    protected String processData(int count, final String data) throws IllegalArgumentException {
        if (count < 0) {
            throw new IllegalArgumentException("Count cannot be negative");
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < count; i++) {
            sb.append(data);
        }
        return sb.toString();
    }

    // A method without Javadoc
    void utilityMethod() {
        // Do something
    }

    private static class NestedClass {
        private int nestedField;

        public void nestedMethod() {}
    }
}
