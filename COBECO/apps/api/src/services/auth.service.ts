import { hash, verify } from 'argon2';
import jwt, { JwtPayload, SignOptions } from 'jsonwebtoken';
import { randomBytes } from 'crypto';
import {
  PasswordResetTokenRepositoryContract,
  UserRepositoryContract,
} from '../repositories/repository.contracts';
import { AppError } from '../types';
import { getAuthSecrets } from '../config/auth-config';

const { sign, verify: verifyToken } = jwt;

export class AuthService {
  constructor(
    private userRepository: UserRepositoryContract,
    private tokenRepository: PasswordResetTokenRepositoryContract
  ) {}

  async signUp(
    name: string,
    username: string,
    email: string,
    password: string,
    consent: boolean
  ) {
    if (consent !== true) {
      throw new AppError(
        'CONSENT_REQUIRED',
        'É necessário aceitar o tratamento dos seus dados para criar a conta',
        400
      );
    }

    email = email.trim().toLowerCase();
    // RF01: o username é único e comparado sem distinção de caixa; guardá-lo já
    // normalizado é o que torna a constraint do banco realmente efetiva.
    username = username.trim().toLowerCase();

    const existingUser = await this.userRepository.findByEmail(email);
    if (existingUser) {
      throw new AppError('EMAIL_ALREADY_REGISTERED', 'Este e-mail já está cadastrado', 400);
    }

    const existingUsername = await this.userRepository.findByUsername(username);
    if (existingUsername) {
      throw new AppError(
        'USERNAME_ALREADY_REGISTERED',
        'Este nome de usuário já está em uso',
        400
      );
    }

    const passwordHash = await hash(password);
    const user = await this.userRepository.create({
      name,
      username,
      email,
      passwordHash,
    });

    return {
      id: user.id,
      name: user.name,
      username: user.username,
      email: user.email,
    };
  }

  /** RF02: `identifier` é o e-mail ou o username do usuário. */
  async login(identifier: string, password: string) {
    const user = await this.userRepository.findByEmailOrUsername(identifier.trim().toLowerCase());
    if (!user || user.deletedAt) {
      throw new AppError('INVALID_CREDENTIALS', 'Credenciais inválidas', 401);
    }

    const passwordValid = await verify(user.passwordHash, password);
    if (!passwordValid) {
      throw new AppError('INVALID_CREDENTIALS', 'Credenciais inválidas', 401);
    }

    const accessToken = this.generateAccessToken(user.id, user.email);
    const refreshToken = this.generateRefreshToken(user.id, user.email);

    return {
      accessToken,
      refreshToken,
      user: {
        id: user.id,
        name: user.name,
        username: user.username,
        email: user.email,
      },
    };
  }

  async validateAccessToken(token: string) {
    try {
      const payload = verifyToken(token, getAuthSecrets().accessSecret);

      if (typeof payload === 'string' || payload.type !== 'access') {
        throw new AppError('INVALID_TOKEN', 'Token inválido', 401);
      }

      return payload;
    } catch (error) {
      throw new AppError('INVALID_TOKEN', 'Token inválido', 401);
    }
  }

  /**
   * Troca o refresh token (cookie httpOnly) por um novo par de tokens.
   * Sem isto a sessão morre ao fim da validade do access token, mesmo com o
   * usuário ativo.
   */
  async refresh(refreshToken: string | undefined) {
    const expired = new AppError(
      'SESSION_EXPIRED',
      'Sua sessão expirou. Faça login novamente.',
      401
    );

    if (!refreshToken) throw expired;

    let payload: string | JwtPayload;
    try {
      payload = verifyToken(refreshToken, getAuthSecrets().refreshSecret);
    } catch (error) {
      throw expired;
    }

    if (typeof payload === 'string' || payload.type !== 'refresh' || !payload.sub) {
      throw expired;
    }

    const user = await this.userRepository.findById(payload.sub as string);
    if (!user || user.deletedAt) throw expired;

    return {
      accessToken: this.generateAccessToken(user.id, user.email),
      refreshToken: this.generateRefreshToken(user.id, user.email),
      user: {
        id: user.id,
        name: user.name,
        username: user.username,
        email: user.email,
      },
    };
  }

  generateAccessToken(userId: string, email: string): string {
    const expiresIn = process.env.JWT_ACCESS_EXPIRY || '15m';
    return sign({ sub: userId, email, type: 'access' }, getAuthSecrets().accessSecret, {
      expiresIn: expiresIn as SignOptions['expiresIn'],
      algorithm: 'HS256',
    });
  }

  generateRefreshToken(userId: string, email: string): string {
    // A rotação renova a janela; 30 minutos sem atividade invalidam a sessão.
    const expiresIn = process.env.JWT_REFRESH_EXPIRY || '30m';
    return sign({ sub: userId, email, type: 'refresh' }, getAuthSecrets().refreshSecret, {
      expiresIn: expiresIn as SignOptions['expiresIn'],
      algorithm: 'HS256',
    });
  }

  async requestPasswordReset(email: string) {
    // Mesma normalização de signUp/login: sem ela um e-mail digitado com outra
    // caixa nunca encontra o usuário e o pedido falha em silêncio.
    const user = await this.userRepository.findByEmail(email.trim().toLowerCase());
    if (!user || user.deletedAt) {
      // Return success even if user not found (security best practice)
      return { message: 'Se o e-mail existir, você receberá as instruções de redefinição' };
    }

    // Generate token
    const token = randomBytes(32).toString('hex');
    const tokenHash = await hash(token);
    const expiresAt = new Date(Date.now() + 1000 * 60 * 60); // 1 hour

    await this.tokenRepository.create({
      userId: user.id,
      tokenHash,
      expiresAt,
    });

    // In development, log the link to console
    if (process.env.NODE_ENV === 'development') {
      const resetLink = `http://localhost:5173/reset-password?token=${token}`;
      console.log(`[PASSWORD RESET] Link para ${email}: ${resetLink}`);
    }

    return { message: 'Se o e-mail existir, você receberá as instruções de redefinição' };
  }

  async resetPassword(token: string, newPassword: string) {
    const tokenRecord = await this.tokenRepository.findByToken(token);

    if (!tokenRecord || tokenRecord.usedAt || tokenRecord.expiresAt < new Date()) {
      throw new AppError('INVALID_RESET_TOKEN', 'O link de redefinição é inválido ou expirou', 400);
    }

    const passwordHash = await hash(newPassword);
    await this.userRepository.updatePassword(tokenRecord.userId, passwordHash);
    await this.tokenRepository.markAsUsed(tokenRecord.id);

    return { message: 'Senha redefinida com sucesso' };
  }

  async deleteAccount(userId: string) {
    await this.userRepository.softDelete(userId);
    return { message: 'Conta excluída com sucesso' };
  }
}
