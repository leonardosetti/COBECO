export interface AuthPayload {
  id: string;
  email: string;
}

export interface JWTPayload {
  sub: string;
  email: string;
  type: 'access' | 'refresh';
}

export class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number = 400
  ) {
    super(message);
    this.name = 'AppError';
  }
}
