package com.example.enums;

/**
 * Javadoc for SampleEnum.
 * Represents different states.
 */
public enum SampleEnum {
    /**
     * Javadoc for STATE_ONE.
     */
    STATE_ONE(10) {
        @Override
        public String customBehavior() {
            return "Behavior for STATE_ONE";
        }
    },
    /**
     * Javadoc for STATE_TWO.
     */
    STATE_TWO(20),
    STATE_THREE(30); // No Javadoc for this constant

    /**
     * Javadoc for internalValue.
     */
    private final int internalValue;

    /**
     * Javadoc for the enum constructor.
     * @param value The internal value for the enum constant.
     */
    SampleEnum(int value) {
        this.internalValue = value;
    }

    /**
     * Javadoc for getInternalValue.
     * @return The internal value.
     */
    public int getInternalValue() {
        return internalValue;
    }

    /**
     * Javadoc for customBehavior.
     * This method can be overridden by constants.
     * @return A string representing custom behavior.
     */
    public String customBehavior() {
        return "Default behavior";
    }
}
