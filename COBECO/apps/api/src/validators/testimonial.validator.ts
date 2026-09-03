import { z } from 'zod';

export const testimonialSchema = z.object({
  authorName: z.string().trim().min(2, 'Informe seu nome').max(80, 'Nome muito longo'),
  content: z.string().trim().min(10, 'Escreva ao menos 10 caracteres').max(500, 'Depoimento muito longo'),
});
