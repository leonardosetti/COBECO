/* eslint-disable @typescript-eslint/no-explicit-any -- mocks parciais do Prisma */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { AuthService } from './auth.service';
import { UserRepository } from '../repositories/user.repository';
import { PasswordResetTokenRepository } from '../repositories/password-reset-token.repository';

// Mock repositories
const mockUserRepository = {
  create: vi.fn(),
  findByEmail: vi.fn(),
  findByUsername: vi.fn(),
  findByEmailOrUsername: vi.fn(),
  findById: vi.fn(),
  updatePassword: vi.fn(),
  softDelete: vi.fn(),
  updateConsent: vi.fn(),
} as unknown as UserRepository;

const mockTokenRepository = {
  create: vi.fn(),
  findByTokenHash: vi.fn(),
  markAsUsed: vi.fn(),
  deleteExpired: vi.fn(),
} as unknown as PasswordResetTokenRepository;

let authService: AuthService;

beforeEach(() => {
  authService = new AuthService(mockUserRepository, mockTokenRepository);
  vi.clearAllMocks();
});

describe('AuthService', () => {
  describe('signUp', () => {
    it('should create a new user', async () => {
      const mockUser = {
        id: '123',
        name: 'Test User',
        username: 'test_user',
        email: 'test@example.com',
        passwordHash: 'hashed',
        consentedAt: null,
        createdAt: new Date(),
        updatedAt: new Date(),
        deletedAt: null,
      };

      (mockUserRepository.findByEmail as any).mockResolvedValue(null);
      (mockUserRepository.findByUsername as any).mockResolvedValue(null);
      (mockUserRepository.create as any).mockResolvedValue(mockUser);

      const result = await authService.signUp(
        'Test User',
        'Test_User',
        'test@example.com',
        'SecurePass123!',
        true
      );

      expect(result.id).toBe('123');
      expect(result.email).toBe('test@example.com');
      expect(result.username).toBe('test_user');
      expect(mockUserRepository.findByEmail as any).toHaveBeenCalledWith('test@example.com');
      // O username é normalizado antes de checar unicidade (RF01).
      expect(mockUserRepository.findByUsername as any).toHaveBeenCalledWith('test_user');
      expect(mockUserRepository.create as any).toHaveBeenCalled();
    });

    it('should throw error if email already exists', async () => {
      const existingUser = {
        id: '123',
        email: 'test@example.com',
        passwordHash: 'hashed',
      };

      (mockUserRepository.findByEmail as any).mockResolvedValue(existingUser);

      await expect(
        authService.signUp('Test User', 'test_user', 'test@example.com', 'SecurePass123!', true)
      ).rejects.toThrow('Este e-mail já está cadastrado');
    });

    it('should throw error if username already exists', async () => {
      (mockUserRepository.findByEmail as any).mockResolvedValue(null);
      (mockUserRepository.findByUsername as any).mockResolvedValue({ id: '456' });

      await expect(
        authService.signUp('Test User', 'test_user', 'outro@example.com', 'SecurePass123!', true)
      ).rejects.toThrow('Este nome de usuário já está em uso');
    });

    it('should reject sign up without consent', async () => {
      await expect(
        authService.signUp('Test User', 'test_user', 'test@example.com', 'SecurePass123!', false)
      ).rejects.toThrow('É necessário aceitar o tratamento dos seus dados para criar a conta');
    });
  });

  describe('login', () => {
    it('should throw error for invalid credentials', async () => {
      (mockUserRepository.findByEmailOrUsername as any).mockResolvedValue(null);

      await expect(authService.login('test@example.com', 'password')).rejects.toThrow(
        'Credenciais inválidas'
      );
    });

    it('resolves the account by username as well as by email', async () => {
      (mockUserRepository.findByEmailOrUsername as any).mockResolvedValue(null);

      await expect(authService.login('Test_User', 'password')).rejects.toThrow(
        'Credenciais inválidas'
      );
      expect(mockUserRepository.findByEmailOrUsername as any).toHaveBeenCalledWith('test_user');
    });

    it('should throw error if user is deleted', async () => {
      const deletedUser = {
        id: '123',
        email: 'test@example.com',
        passwordHash: 'hashed',
        deletedAt: new Date(),
      };

      (mockUserRepository.findByEmailOrUsername as any).mockResolvedValue(deletedUser);

      await expect(authService.login('test@example.com', 'password')).rejects.toThrow(
        'Credenciais inválidas'
      );
    });
  });

  describe('deleteAccount', () => {
    it('should soft delete user account', async () => {
      const deletedUser = {
        id: '123',
        deletedAt: new Date(),
      };

      (mockUserRepository.softDelete as any).mockResolvedValue(deletedUser);

      const result = await authService.deleteAccount('123');

      expect(mockUserRepository.softDelete as any).toHaveBeenCalledWith('123');
      expect(result.message).toBe('Conta excluída com sucesso');
    });
  });
});
