/**
 * Modal Component Types
 * Simple, composable modal interface
 */

import { ReactNode } from 'react';

export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

export interface ModalProps {
  /** Whether the modal is open */
  open: boolean;

  /** Callback when modal should close */
  onClose: () => void;

  /** Modal title */
  title?: string;

  /** Modal content */
  children: ReactNode;

  /** Size variant */
  size?: ModalSize;

  /** Show close button in header */
  showClose?: boolean;

  /** Footer content */
  footer?: ReactNode;

  /** Prevent closing on backdrop click */
  preventBackdropClose?: boolean;
}
