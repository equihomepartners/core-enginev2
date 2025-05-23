/**
 * Format a number as currency
 * @param value Number to format
 * @returns Formatted currency string
 */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

/**
 * Format a number as percentage
 * @param value Number to format (0-1)
 * @returns Formatted percentage string
 */
export function formatPercentage(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value);
}

/**
 * Format a number as a decimal
 * @param value Number to format
 * @param decimals Number of decimal places
 * @returns Formatted decimal string
 */
export function formatDecimal(value: number, decimals: number = 2): string {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value);
}

/**
 * Format a date
 * @param date Date to format
 * @param options Intl.DateTimeFormatOptions
 * @returns Formatted date string
 */
export function formatDate(
  date: Date | string | number,
  options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }
): string {
  const dateObj = typeof date === 'object' ? date : new Date(date);
  return new Intl.DateTimeFormat('en-US', options).format(dateObj);
}

/**
 * Format a number as a compact number (e.g., 1.2M)
 * @param value Number to format
 * @returns Formatted compact number string
 */
export function formatCompactNumber(value: number): string {
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    compactDisplay: 'short'
  }).format(value);
}

/**
 * Format a number as basis points
 * @param value Number of basis points
 * @returns Formatted basis points string
 */
export function formatBasisPoints(value: number): string {
  return `${value.toFixed(0)} bps`;
}

export default {
  formatCurrency,
  formatPercentage,
  formatDecimal,
  formatDate,
  formatCompactNumber,
  formatBasisPoints
};
