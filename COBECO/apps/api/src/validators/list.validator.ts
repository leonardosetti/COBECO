import { z } from 'zod';

const itemFields = {
  description: z.string().trim().min(1, 'Descreva o produto').max(160, 'Descrição muito longa'),
  quantity: z.number().int().min(1, 'A quantidade mínima é 1').max(999, 'Quantidade máxima: 999'),
  productId: z.string().trim().min(1).nullable().optional(),
};

export const createListSchema = z.object({
  name: z.string().trim().min(1, 'Informe um nome para a lista').max(80, 'Nome muito longo'),
  categoryId: z.string().trim().min(1).nullable().optional(),
});

export const updateListSchema = createListSchema.pick({ name: true });

/** O nome é opcional: sem ele o controller deriva "<nome original> (cópia)". */
export const duplicateListSchema = z.object({
  name: createListSchema.shape.name.optional(),
});

export const createListItemSchema = z.object({
  description: itemFields.description,
  quantity: itemFields.quantity.default(1),
  productId: itemFields.productId,
});

export const updateListItemSchema = createListItemSchema;

export const bulkListItemsSchema = z.union([
  z.object({
    lines: z.string().trim().min(1, 'Informe ao menos um produto').max(10_000, 'Texto muito longo'),
  }),
  z.object({
    items: z
      .array(createListItemSchema)
      .min(1, 'Informe ao menos um produto')
      .max(100, 'Limite de 100 produtos por lote'),
  }),
]);
