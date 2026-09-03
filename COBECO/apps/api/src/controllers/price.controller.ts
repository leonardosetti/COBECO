import { Request, Response, NextFunction } from 'express';
import { PriceIntegrationService } from '../integrations/price.service';

export class PriceController {
  constructor(private readonly priceService: PriceIntegrationService) {}

  async search(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.priceService.search(req.query.q as string));
    } catch (error) {
      next(error);
    }
  }
}
