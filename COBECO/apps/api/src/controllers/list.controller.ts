import { Request, Response, NextFunction } from 'express';
import { AppError } from '../types';
import { ListService } from '../services/list.service';

export class ListController {
  constructor(private readonly listService: ListService) {}

  private getUserId(req: Request): string {
    if (!req.user?.id) throw new AppError('UNAUTHORIZED', 'Usuário não autenticado', 401);
    return req.user.id;
  }

  async list(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.listService.list(this.getUserId(req)));
    } catch (error) {
      next(error);
    }
  }

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      res
        .status(201)
        .json(
          await this.listService.create(this.getUserId(req), req.body.name, req.body.categoryId)
        );
    } catch (error) {
      next(error);
    }
  }

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.listService.update(this.getUserId(req), req.params.listId, req.body.name)
      );
    } catch (error) {
      next(error);
    }
  }

  async remove(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(await this.listService.remove(this.getUserId(req), req.params.listId));
    } catch (error) {
      next(error);
    }
  }

  async duplicate(req: Request, res: Response, next: NextFunction) {
    try {
      const name =
        req.body.name ||
        `${
          (await this.listService.list(this.getUserId(req))).find(
            (list) => list.id === req.params.listId
          )?.name || 'Lista'
        } (cópia)`;
      res
        .status(201)
        .json(await this.listService.duplicate(this.getUserId(req), req.params.listId, name));
    } catch (error) {
      next(error);
    }
  }

  async addItem(req: Request, res: Response, next: NextFunction) {
    try {
      res
        .status(201)
        .json(
          await this.listService.addItem(
            this.getUserId(req),
            req.params.listId,
            req.body.description,
            req.body.quantity,
            req.body.productId
          )
        );
    } catch (error) {
      next(error);
    }
  }

  async addBulkItems(req: Request, res: Response, next: NextFunction) {
    try {
      const items =
        req.body.items ||
        req.body.lines.split(/\r?\n/).map((description: string) => ({ description, quantity: 1 }));
      const validItems = items.filter((item: { description: string }) => item.description.trim());
      if (!validItems.length) throw new AppError('EMPTY_ITEMS', 'Informe ao menos um produto', 400);
      res
        .status(201)
        .json(await this.listService.addItems(this.getUserId(req), req.params.listId, validItems));
    } catch (error) {
      next(error);
    }
  }

  async updateItem(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.listService.updateItem(
          this.getUserId(req),
          req.params.listId,
          req.params.itemId,
          req.body.description,
          req.body.quantity,
          req.body.productId
        )
      );
    } catch (error) {
      next(error);
    }
  }

  async removeItem(req: Request, res: Response, next: NextFunction) {
    try {
      res.json(
        await this.listService.removeItem(this.getUserId(req), req.params.listId, req.params.itemId)
      );
    } catch (error) {
      next(error);
    }
  }
}
