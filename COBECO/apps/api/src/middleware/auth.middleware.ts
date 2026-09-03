import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { getAuthSecrets } from '../config/auth-config';

const { verify } = jwt;

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: {
        code: 'MISSING_TOKEN',
        message: 'Token não fornecido',
      },
    });
  }

  const token = authHeader.substring(7);

  try {
    const payload = verify(token, getAuthSecrets().accessSecret);

    if (typeof payload === 'string') {
      throw new Error('Invalid payload');
    }

    // O refresh token tem validade de 7 dias e circula em cookie; aceitá-lo aqui
    // transformaria a sessão longa em credencial de acesso.
    if (payload.type !== 'access') {
      throw new Error('Unexpected token type');
    }

    req.user = {
      id: payload.sub as string,
      email: payload.email as string,
    };

    next();
  } catch (error) {
    return res.status(401).json({
      error: {
        code: 'INVALID_TOKEN',
        message: 'Token inválido',
      },
    });
  }
}
