import { Router } from 'express';
import { authMiddleware } from '../middleware/auth.middleware';
import { AuthController } from '../controllers/auth.controller';
import { ListController } from '../controllers/list.controller';
import { validateBody, validateQuery } from '../middleware/validation.middleware';
import {
  bulkListItemsSchema,
  createListItemSchema,
  createListSchema,
  duplicateListSchema,
  updateListItemSchema,
  updateListSchema,
} from '../validators/list.validator';
import { PriceController } from '../controllers/price.controller';
import { priceSearchSchema } from '../validators/price.validator';
import { QuotationController } from '../controllers/quotation.controller';
import {
  compareQuotationSchema,
  historyQuerySchema,
  quoteItemSchema,
  quoteListSchema,
} from '../validators/quotation.validator';
import { ShareController } from '../controllers/share.controller';
import { TestimonialController } from '../controllers/testimonial.controller';
import { testimonialSchema } from '../validators/testimonial.validator';
import { CatalogController } from '../controllers/catalog.controller';

export function createPlatformRoutes(
  authController: AuthController,
  listController: ListController,
  priceController: PriceController,
  quotationController: QuotationController,
  shareController: ShareController,
  testimonialController: TestimonialController,
  catalogController: CatalogController
): Router {
  const router = Router();

  // All routes under /api/platform require authentication
  router.use(authMiddleware);

  router.delete('/account', (req, res, next) => authController.deleteAccount(req, res, next));

  router.get('/categories', (req, res, next) => catalogController.categories(req, res, next));
  router.get('/categories/:id/suppliers', (req, res, next) =>
    catalogController.suppliers(req, res, next)
  );
  router.get('/categories/:id/products', (req, res, next) =>
    catalogController.products(req, res, next)
  );

  router.get('/prices/search', validateQuery(priceSearchSchema), (req, res, next) =>
    priceController.search(req, res, next)
  );
  router.post('/quotations/item', validateBody(quoteItemSchema), (req, res, next) =>
    quotationController.quoteItem(req, res, next)
  );
  router.post('/testimonials', validateBody(testimonialSchema), (req, res, next) =>
    testimonialController.create(req, res, next)
  );
  router.get('/quotations/history', validateQuery(historyQuerySchema), (req, res, next) =>
    quotationController.history(req, res, next)
  );
  router.get('/quotations/compare', validateQuery(compareQuotationSchema), (req, res, next) =>
    quotationController.compare(req, res, next)
  );
  router.get('/quotations/:quotationId', (req, res, next) =>
    quotationController.reopen(req, res, next)
  );
  router.delete('/quotations/:quotationId', (req, res, next) =>
    quotationController.remove(req, res, next)
  );
  router.get('/lists/:listId/suppliers', (req, res, next) =>
    quotationController.listSuppliers(req, res, next)
  );
  router.post('/lists/:listId/quote', validateBody(quoteListSchema), (req, res, next) =>
    quotationController.quoteList(req, res, next)
  );
  router.post('/lists/:listId/share', (req, res, next) => shareController.create(req, res, next));
  router.delete('/lists/:listId/share', (req, res, next) => shareController.revoke(req, res, next));

  router.get('/lists', (req, res, next) => listController.list(req, res, next));
  router.post('/lists', validateBody(createListSchema), (req, res, next) =>
    listController.create(req, res, next)
  );
  router.patch('/lists/:listId', validateBody(updateListSchema), (req, res, next) =>
    listController.update(req, res, next)
  );
  router.delete('/lists/:listId', (req, res, next) => listController.remove(req, res, next));
  router.post('/lists/:listId/duplicate', validateBody(duplicateListSchema), (req, res, next) =>
    listController.duplicate(req, res, next)
  );
  router.post('/lists/:listId/items/bulk', validateBody(bulkListItemsSchema), (req, res, next) =>
    listController.addBulkItems(req, res, next)
  );
  router.post('/lists/:listId/items', validateBody(createListItemSchema), (req, res, next) =>
    listController.addItem(req, res, next)
  );
  router.patch(
    '/lists/:listId/items/:itemId',
    validateBody(updateListItemSchema),
    (req, res, next) => listController.updateItem(req, res, next)
  );
  router.delete('/lists/:listId/items/:itemId', (req, res, next) =>
    listController.removeItem(req, res, next)
  );

  return router;
}
