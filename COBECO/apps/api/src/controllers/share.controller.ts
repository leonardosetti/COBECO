import { Request, Response, NextFunction } from 'express';
import { AppError } from '../types';
import { ShareService } from '../services/share.service';

export class ShareController {
  constructor(private readonly shareService: ShareService) {}

  private userId(req: Request): string {
    if (!req.user?.id) throw new AppError('UNAUTHORIZED', 'Usuário não autenticado', 401);
    return req.user.id;
  }

  async create(req: Request, res: Response, next: NextFunction) {
    try { res.status(201).json(await this.shareService.create(this.userId(req), req.params.listId)); }
    catch (error) { next(error); }
  }

  async revoke(req: Request, res: Response, next: NextFunction) {
    try { res.json(await this.shareService.revoke(this.userId(req), req.params.listId)); }
    catch (error) { next(error); }
  }

  async getPublic(req: Request, res: Response, next: NextFunction) {
    try { res.json(await this.shareService.getSharedList(req.params.token)); }
    catch (error) { next(error); }
  }
}
