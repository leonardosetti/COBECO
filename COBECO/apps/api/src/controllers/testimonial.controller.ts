import { Request, Response, NextFunction } from 'express';
import { AppError } from '../types';
import { TestimonialRepositoryContract } from '../repositories/repository.contracts';

export class TestimonialController {
  constructor(private readonly testimonialRepository: TestimonialRepositoryContract) {}

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      if (!req.user?.id) throw new AppError('UNAUTHORIZED', 'Usuário não autenticado', 401);
      res.status(201).json(await this.testimonialRepository.create({ userId: req.user.id, authorName: req.body.authorName, content: req.body.content }));
    } catch (error) {
      next(error);
    }
  }
}
