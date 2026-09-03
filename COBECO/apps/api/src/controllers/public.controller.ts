import { Request, Response, NextFunction } from 'express';
import {
  RetailerRepositoryContract,
  TestimonialRepositoryContract,
} from '../repositories/repository.contracts';

export class PublicController {
  constructor(
    private testimonialRepository: TestimonialRepositoryContract,
    private retailerRepository: RetailerRepositoryContract
  ) {}

  async getTestimonials(_req: Request, res: Response, next: NextFunction) {
    try {
      const testimonials = await this.testimonialRepository.findApproved();
      res.json(testimonials);
    } catch (error) {
      next(error);
    }
  }

  async getRetailers(_req: Request, res: Response, next: NextFunction) {
    try {
      const retailers = await this.retailerRepository.findAll();
      res.json(retailers);
    } catch (error) {
      next(error);
    }
  }
}
