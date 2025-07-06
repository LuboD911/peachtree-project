// API Response Types
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  status?: number;
}

// Auth Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

// Transaction Types
export interface Contractor {
  id: number;
  name: string;
  image_url?: string;
}

export interface SystemAccount {
  id: number;
  name: string;
  balance: number;
}

export interface Status {
  id: number;
  name: string;
  color?: string;
}

export interface Transaction {
  id: number;
  date: string;
  amount: number;
  contractor: Contractor;
  status: Status;
  type?: string;
  account_id?: number;
}

export interface CreateTransactionRequest {
  contractor_id: string;
  type: string;
  amount: number;
  account_id: string;
}

export interface UpdateTransactionStatusRequest {
  status_id: number;
}

// Component Props Types
export interface TransactionFormProps {
  // No props needed
}

export interface TransactionListProps {
  // No props needed
}

export interface TransactionDetailProps {
  transactionId: number;
}

export interface TransactionStatusDropdownProps {
  currentStatusId: number;
}

export interface HelloWorldProps {
  msg: string;
}

// Component Emits Types
export interface TransactionFormEmits {
  transactionCreated: () => void;
}

export interface TransactionListEmits {
  select: (id: number) => void;
}

export interface TransactionDetailEmits {
  close: () => void;
}

export interface TransactionStatusDropdownEmits {
  change: (value: number) => void;
}

// Form Types
export interface LoginForm {
  username: string;
  password: string;
}

export interface RegisterForm {
  username: string;
  password: string;
  confirmPassword: string;
}

// Error Types
export interface ApiError {
  response?: {
    data?: {
      message?: string;
    };
    status?: number;
  };
  message?: string;
}

// Environment Types
export interface ImportMetaEnv {
  VITE_API_URL: string;
}

// Axios Types
export interface AxiosRequestConfig {
  _retry?: boolean;
  headers?: Record<string, string>;
  params?: Record<string, any>;
}

// Event Types
export interface InputEvent extends Event {
  target: HTMLInputElement;
}

export interface SelectEvent extends Event {
  target: HTMLSelectElement;
}

export interface KeyboardEvent extends Event {
  key: string;
  metaKey: boolean;
  ctrlKey: boolean;
} 