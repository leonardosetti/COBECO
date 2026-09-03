import { z } from 'zod';

/** RF01: mínimo 8 caracteres, com maiúscula, minúscula, número e especial. */
const passwordSchema = z
  .string()
  .min(8, 'Senha deve ter no mínimo 8 caracteres')
  .regex(/[A-Z]/, 'Senha deve conter pelo menos uma letra maiúscula')
  .regex(/[a-z]/, 'Senha deve conter pelo menos uma letra minúscula')
  .regex(/\d/, 'Senha deve conter pelo menos um número')
  .regex(/[^A-Za-z0-9]/, 'Senha deve conter pelo menos um caractere especial');

export const usernameSchema = z
  .string()
  .trim()
  .min(3, 'Nome de usuário deve ter no mínimo 3 caracteres')
  .max(30, 'Nome de usuário deve ter no máximo 30 caracteres')
  .regex(/^[A-Za-z0-9_]+$/, 'Nome de usuário aceita apenas letras, números e underscore');

export const signUpSchema = z.object({
  name: z
    .string()
    .trim()
    .min(2, 'Nome deve ter no mínimo 2 caracteres')
    .max(100, 'Nome deve ter no máximo 100 caracteres'),
  username: usernameSchema,
  email: z.string().email('E-mail inválido').max(255, 'E-mail deve ter no máximo 255 caracteres'),
  password: passwordSchema,
  // LGPD: o consentimento precisa ser manifestado, não presumido no cadastro.
  consent: z.literal(true, {
    errorMap: () => ({ message: 'É necessário aceitar o tratamento dos seus dados' }),
  }),
});

export const loginSchema = z
  .object({
    // RF02: o acesso aceita e-mail ou username. `email` continua sendo aceito
    // para não quebrar clientes que já enviavam esse campo.
    identifier: z.string().trim().min(1).optional(),
    email: z.string().trim().min(1).optional(),
    password: z.string().min(1, 'Senha é obrigatória'),
  })
  .refine((value) => Boolean(value.identifier || value.email), {
    message: 'Informe seu e-mail ou nome de usuário',
    path: ['identifier'],
  });

export const requestPasswordResetSchema = z.object({
  email: z.string().email('E-mail inválido'),
});

export const resetPasswordSchema = z.object({
  token: z.string().min(1, 'Token é obrigatório'),
  newPassword: passwordSchema,
});

export type SignUpRequest = z.infer<typeof signUpSchema>;
export type LoginRequest = z.infer<typeof loginSchema>;
export type RequestPasswordResetRequest = z.infer<typeof requestPasswordResetSchema>;
export type ResetPasswordRequest = z.infer<typeof resetPasswordSchema>;
