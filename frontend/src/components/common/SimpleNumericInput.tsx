import React, { useState, useEffect } from 'react';
import { Intent } from '@blueprintjs/core';

interface SimpleNumericInputProps {
  value: number;
  onValueChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
  formatter?: (value: number) => string;
  intent?: Intent;
  fill?: boolean;
  disabled?: boolean;
  placeholder?: string;
  onBlur?: () => void;
}

/**
 * A simple numeric input component that doesn't use Blueprint's InputGroup
 * to avoid the infinite update loop issue
 */
const SimpleNumericInput: React.FC<SimpleNumericInputProps> = ({
  value,
  onValueChange,
  min = Number.MIN_SAFE_INTEGER,
  max = Number.MAX_SAFE_INTEGER,
  step = 1,
  formatter,
  intent = Intent.NONE,
  fill = false,
  disabled = false,
  placeholder = '',
  onBlur
}) => {
  const [inputValue, setInputValue] = useState<string>('');
  
  // Update the input value when the prop value changes
  useEffect(() => {
    if (formatter && typeof value === 'number') {
      setInputValue(formatter(value));
    } else {
      setInputValue(value?.toString() || '');
    }
  }, [value, formatter]);
  
  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };
  
  // Handle blur - convert the input value to a number and clamp it
  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    let numValue = parseFloat(e.target.value.replace(/[^0-9.-]/g, ''));
    
    if (isNaN(numValue)) {
      numValue = 0;
    }
    
    // Clamp the value between min and max
    const clampedValue = Math.max(min, Math.min(max, numValue));
    
    // Update the parent component
    onValueChange(clampedValue);
    
    // Call the onBlur callback if provided
    if (onBlur) {
      onBlur();
    }
  };
  
  // Handle focus - show the raw value
  const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    e.target.value = value?.toString() || '';
    e.target.select();
  };
  
  // Handle increment/decrement buttons
  const increment = () => {
    const newValue = Math.min(max, value + step);
    onValueChange(newValue);
  };
  
  const decrement = () => {
    const newValue = Math.max(min, value - step);
    onValueChange(newValue);
  };
  
  // Get the intent class
  const getIntentClass = () => {
    switch (intent) {
      case Intent.PRIMARY:
        return 'border-blue-500 focus:border-blue-500 focus:ring-blue-500';
      case Intent.SUCCESS:
        return 'border-green-500 focus:border-green-500 focus:ring-green-500';
      case Intent.WARNING:
        return 'border-yellow-500 focus:border-yellow-500 focus:ring-yellow-500';
      case Intent.DANGER:
        return 'border-red-500 focus:border-red-500 focus:ring-red-500';
      default:
        return 'border-gray-300 focus:border-blue-500 focus:ring-blue-500';
    }
  };
  
  return (
    <div className={`flex ${fill ? 'w-full' : ''}`}>
      <button
        type="button"
        onClick={decrement}
        disabled={disabled || value <= min}
        className="px-2 py-1 bg-gray-200 border border-gray-300 rounded-l-md hover:bg-gray-300 disabled:opacity-50"
      >
        -
      </button>
      <input
        type="text"
        value={inputValue}
        onChange={handleChange}
        onBlur={handleBlur}
        onFocus={handleFocus}
        disabled={disabled}
        placeholder={placeholder}
        className={`px-2 py-1 border ${getIntentClass()} focus:outline-none focus:ring-2 ${fill ? 'w-full' : 'w-24'}`}
      />
      <button
        type="button"
        onClick={increment}
        disabled={disabled || value >= max}
        className="px-2 py-1 bg-gray-200 border border-gray-300 rounded-r-md hover:bg-gray-300 disabled:opacity-50"
      >
        +
      </button>
    </div>
  );
};

export default SimpleNumericInput;
