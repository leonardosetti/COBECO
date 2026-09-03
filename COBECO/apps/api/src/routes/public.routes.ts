import { Router } from 'express';
import { PublicController } from '../controllers/public.controller';
import { ShareController } from '../controllers/share.controller';

export function createPublicRoutes(publicController: PublicController, shareController: ShareController): Router {
  const router = Router();

  router.get('/testimonials', (req, res, next) =>
    publicController.getTestimonials(req, res, next)
  );

  router.get('/retailers', (req, res, next) => publicController.getRetailers(req, res, next));
  router.get('/shared-lists/:token', (req, res, next) => shareController.getPublic(req, res, next));

  return router;
}
