import { NextFunction, Request, Response } from 'express';
import { CatalogRepositoryContract } from '../repositories/repository.contracts';

export class CatalogController {
  constructor(private readonly catalogRepository: CatalogRepositoryContract) {}

  async categories(_req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.catalogRepository.findCategories());
    } catch (error) {
      next(error);
    }
  }

  async suppliers(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.catalogRepository.findSuppliersByCategory(req.params.id));
    } catch (error) {
      next(error);
    }
  }

  async products(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.catalogRepository.findProductsByCategory(req.params.id));
    } catch (error) {
      next(error);
    }
  }
}
