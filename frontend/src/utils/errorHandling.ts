import { toast } from '../api/toast';

/**
 * Error types for better error handling
 */
export enum ErrorType {
  NETWORK = 'network',
  VALIDATION = 'validation',
  AUTHENTICATION = 'authentication',
  AUTHORIZATION = 'authorization',
  NOT_FOUND = 'not_found',
  SERVER = 'server',
  UNKNOWN = 'unknown',
}

/**
 * Custom error class with additional properties
 */
export class AppError extends Error {
  type: ErrorType;
  statusCode?: number;
  details?: any;

  constructor(message: string, type: ErrorType = ErrorType.UNKNOWN, statusCode?: number, details?: any) {
    super(message);
    this.name = 'AppError';
    this.type = type;
    this.statusCode = statusCode;
    this.details = details;
  }
}

/**
 * Parse error from API response
 * @param error Error object from API call
 * @returns AppError with appropriate type and details
 */
export function parseApiError(error: any): AppError {
  // Network error (no response)
  if (error.request && !error.response) {
    return new AppError(
      'Network error. Please check your connection.',
      ErrorType.NETWORK
    );
  }

  // Server responded with an error
  if (error.response) {
    const { status, data } = error.response;

    // Authentication error
    if (status === 401) {
      return new AppError(
        'Authentication failed. Please log in again.',
        ErrorType.AUTHENTICATION,
        status
      );
    }

    // Authorization error
    if (status === 403) {
      return new AppError(
        'You do not have permission to perform this action.',
        ErrorType.AUTHORIZATION,
        status
      );
    }

    // Not found
    if (status === 404) {
      return new AppError(
        'The requested resource was not found.',
        ErrorType.NOT_FOUND,
        status
      );
    }

    // Validation error
    if (status === 422 && data.detail) {
      return new AppError(
        'Validation error. Please check your input.',
        ErrorType.VALIDATION,
        status,
        data.detail
      );
    }

    // Server error
    if (status >= 500) {
      return new AppError(
        'A server error occurred. Please try again later.',
        ErrorType.SERVER,
        status,
        data
      );
    }

    // Other HTTP errors
    return new AppError(
      data.detail || 'An error occurred. Please try again.',
      ErrorType.UNKNOWN,
      status,
      data
    );
  }

  // Unknown error
  return new AppError(
    error.message || 'An unexpected error occurred.',
    ErrorType.UNKNOWN
  );
}

/**
 * Handle error and show appropriate toast message
 * @param error Error object
 * @param customMessage Optional custom message to show
 */
export function handleError(error: any, customMessage?: string): void {
  console.error('Error:', error);

  const appError = error instanceof AppError ? error : parseApiError(error);

  // Show toast based on error type
  switch (appError.type) {
    case ErrorType.NETWORK:
      toast.error(customMessage || appError.message);
      break;
    case ErrorType.VALIDATION:
      if (appError.details) {
        // Format validation errors
        const messages = Array.isArray(appError.details)
          ? appError.details.map((err: any) => err.msg).join(', ')
          : appError.details;
        toast.error(customMessage || `Validation error: ${messages}`);
      } else {
        toast.error(customMessage || appError.message);
      }
      break;
    case ErrorType.AUTHENTICATION:
      toast.error(customMessage || appError.message);
      // Redirect to login if needed
      break;
    case ErrorType.AUTHORIZATION:
      toast.error(customMessage || appError.message);
      break;
    case ErrorType.NOT_FOUND:
      toast.error(customMessage || appError.message);
      break;
    case ErrorType.SERVER:
      toast.error(customMessage || appError.message);
      break;
    default:
      toast.error(customMessage || 'An unexpected error occurred. Please try again.');
  }
}

/**
 * Format validation errors from Zod
 * @param errors Zod validation errors
 * @returns Formatted error message
 */
export function formatValidationErrors(errors: any): string {
  if (!errors) return 'Validation error';

  const messages: string[] = [];

  // Extract error messages from Zod error format
  Object.entries(errors).forEach(([field, error]: [string, any]) => {
    if (field !== '_errors' && typeof error === 'object') {
      if (error._errors && error._errors.length > 0) {
        messages.push(`${field}: ${error._errors.join(', ')}`);
      }
      
      // Handle nested errors
      Object.entries(error).forEach(([nestedField, nestedError]: [string, any]) => {
        if (nestedField !== '_errors' && typeof nestedError === 'object' && nestedError._errors) {
          messages.push(`${field}.${nestedField}: ${nestedError._errors.join(', ')}`);
        }
      });
    }
  });

  return messages.length > 0 ? messages.join('; ') : 'Validation error';
}
