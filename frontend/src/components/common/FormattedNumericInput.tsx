import React, { useState, useEffect, useRef } from 'react';
import { NumericInput, NumericInputProps } from '@blueprintjs/core';

interface FormattedNumericInputProps extends Omit<NumericInputProps, 'value' | 'onValueChange'> {
  value: number;
  onValueChange: (value: number) => void;
  formatter?: (value: number) => string;
}

/**
 * A wrapper around Blueprint's NumericInput that handles formatting
 * without passing the formatter directly to the DOM
 */
const FormattedNumericInput: React.FC<FormattedNumericInputProps> = ({
  value,
  onValueChange,
  formatter,
  ...props
}) => {
  // Use a ref to store the formatted value
  const formattedValueRef = useRef<string>('');

  // Format the value when it changes
  useEffect(() => {
    if (formatter && typeof value === 'number') {
      formattedValueRef.current = formatter(value);
    } else {
      formattedValueRef.current = value?.toString() || '';
    }
  }, [value, formatter]);

  // Create a custom onValueRender function for NumericInput
  const handleValueRender = (val: number): string => {
    if (formatter && typeof val === 'number') {
      return formatter(val);
    }
    return val?.toString() || '';
  };

  return (
    <NumericInput
      {...props}
      value={value}
      onValueChange={onValueChange}
      valueRenderer={handleValueRender}
    />
  );
};

export default FormattedNumericInput;
