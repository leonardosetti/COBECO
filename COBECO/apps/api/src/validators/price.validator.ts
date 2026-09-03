import { z } from 'zod';

export const priceSearchSchema = z.object({
  q: z.string().trim().min(2, 'Informe ao menos 2 caracteres para pesquisar').max(160, 'Termo de pesquisa muito longo'),
});
