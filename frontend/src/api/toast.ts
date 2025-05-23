import { OverlayToaster, Position, Intent } from '@blueprintjs/core';

// Create a singleton toaster instance
const AppToaster = OverlayToaster.createAsync({
  position: Position.TOP,
  maxToasts: 3,
});

// Toast utility functions
export const toast = {
  /**
   * Show a success toast message
   * @param message Message to display
   * @param timeout Timeout in milliseconds (default: 3000)
   */
  success: async (message: string, timeout = 3000) => {
    const toaster = await AppToaster;
    toaster.show({
      message,
      intent: Intent.SUCCESS,
      icon: 'tick',
      timeout,
    });
  },

  /**
   * Show an info toast message
   * @param message Message to display
   * @param timeout Timeout in milliseconds (default: 5000)
   */
  info: async (message: string, timeout = 5000) => {
    const toaster = await AppToaster;
    toaster.show({
      message,
      intent: Intent.PRIMARY,
      icon: 'info-sign',
      timeout,
    });
  },

  /**
   * Show a warning toast message
   * @param message Message to display
   * @param timeout Timeout in milliseconds (default: 5000)
   */
  warning: async (message: string, timeout = 5000) => {
    const toaster = await AppToaster;
    toaster.show({
      message,
      intent: Intent.WARNING,
      icon: 'warning-sign',
      timeout,
    });
  },

  /**
   * Show an error toast message
   * @param message Message to display
   * @param timeout Timeout in milliseconds (default: 8000)
   */
  error: async (message: string, timeout = 8000) => {
    const toaster = await AppToaster;
    toaster.show({
      message,
      intent: Intent.DANGER,
      icon: 'error',
      timeout,
    });
  },
};

export default toast;
