import { z } from 'zod';

export const quoteItemSchema = z.object({
  description: z
    .string()
    .trim()
    .min(2, 'Informe ao menos 2 caracteres para cotar')
    .max(160, 'Descrição muito longa'),
});

// RF11: a comparação exige de 2 a 10 fornecedores escolhidos pelo usuário.
export const MIN_SUPPLIERS = 2;
export const MAX_SUPPLIERS = 10;

export const quoteListSchema = z.object({
  supplierIds: z
    .array(z.string().trim().min(1))
    .min(MIN_SUPPLIERS, `Selecione ao menos ${MIN_SUPPLIERS} fornecedores para comparar`)
    .max(MAX_SUPPLIERS, `Selecione no máximo ${MAX_SUPPLIERS} fornecedores por comparação`),
});

export const compareQuotationSchema = z
  .object({
    firstId: z.string().trim().min(1, 'Informe a primeira cotação'),
    secondId: z.string().trim().min(1, 'Informe a segunda cotação'),
  })
  .refine((value) => value.firstId !== value.secondId, {
    message: 'Selecione duas cotações diferentes',
  });

export const historyQuerySchema = z.object({
  page: z.coerce.number().int().min(1, 'Página inválida').default(1),
  pageSize: z.coerce
    .number()
    .int()
    .min(1, 'Tamanho de página inválido')
    .max(50, 'O limite é de 50 registros por página')
    .default(20),
});
