import { Request, Response, NextFunction } from 'express';
import { AppError } from '../types';
import { QuotationService } from '../services/quotation.service';

export class QuotationController {
  constructor(private readonly quotationService: QuotationService) {}

  private getUserId(req: Request): string {
    if (!req.user?.id) throw new AppError('UNAUTHORIZED', 'Usuário não autenticado', 401);
    return req.user.id;
  }

  async quoteItem(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.quotationService.quoteItem(this.getUserId(req), req.body.description));
    } catch (error) {
      next(error);
    }
  }

  async quoteList(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.quotationService.quoteList(
          this.getUserId(req),
          req.params.listId,
          req.body.supplierIds
        )
      );
    } catch (error) {
      next(error);
    }
  }

  /** RF12: fornecedores da categoria com o percentual de itens que atendem. */
  async listSuppliers(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.quotationService.listSupplierAvailability(
          this.getUserId(req),
          req.params.listId
        )
      );
    } catch (error) {
      next(error);
    }
  }

  async history(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.quotationService.listHistory(
          this.getUserId(req),
          req.query.page as unknown as number,
          req.query.pageSize as unknown as number
        )
      );
    } catch (error) {
      next(error);
    }
  }

  async reopen(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.quotationService.getHistory(this.getUserId(req), req.params.quotationId));
    } catch (error) {
      next(error);
    }
  }

  async remove(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.quotationService.deleteHistory(this.getUserId(req), req.params.quotationId)
      );
    } catch (error) {
      next(error);
    }
  }

  async compare(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.quotationService.compareHistory(
          this.getUserId(req),
          req.query.firstId as string,
          req.query.secondId as string
        )
      );
    } catch (error) {
      next(error);
    }
  }
}
