// Shared types and validation schemas for COBECO

// User types
export interface User {
  id: string;
  name: string;
  email: string;
  passwordHash: string;
  consentedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}

// Auth DTOs
export interface SignUpRequest {
  name: string;
  email: string;
  password: string;
}

export interface SignUpResponse {
  id: string;
  name: string;
  email: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  accessToken: string;
  user: {
    id: string;
    name: string;
    email: string;
  };
}

export interface RequestPasswordResetRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  newPassword: string;
}

// Error response
export interface ErrorResponse {
  error: {
    code: string;
    message: string;
  };
}

// Testimonial
export interface Testimonial {
  id: string;
  authorName: string;
  content: string;
  approved: boolean;
  createdAt: Date;
}

// Retailer
export interface Retailer {
  id: string;
  name: string;
  slug: string;
  websiteUrl: string;
}

// Product for display
export interface Product {
  id: string;
  name: string;
  description?: string;
  retailer: Retailer;
  price: number;
  deliveryDays: number;
}

// Product lists
export interface ListItem {
  id: string;
  listId: string;
  description: string;
  quantity: number;
  createdAt: Date;
}

export interface ProductList {
  id: string;
  userId: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
  items: ListItem[];
}

export interface CreateListRequest {
  name: string;
}

export interface UpdateListRequest {
  name: string;
}

export interface CreateListItemRequest {
  description: string;
  quantity?: number;
}

export interface BulkListItemsRequest {
  lines?: string;
  items?: CreateListItemRequest[];
}

export interface UpdateListItemRequest {
  description: string;
  quantity: number;
}
