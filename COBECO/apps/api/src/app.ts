import express, { Express } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import { AuthController } from './controllers/auth.controller';
import { PublicController } from './controllers/public.controller';
import { ListController } from './controllers/list.controller';
import { AuthService } from './services/auth.service';
import {
  MemoryListRepository,
  MemoryPasswordResetTokenRepository,
  MemoryRetailerRepository,
  MemoryTestimonialRepository,
  MemoryUserRepository,
  MemoryQuotationRepository,
  MemoryCatalogRepository,
} from './repositories/memory.repository';
import { ListService } from './services/list.service';
import { createAuthRoutes } from './routes/auth.routes';
import { createPublicRoutes } from './routes/public.routes';
import { createPlatformRoutes } from './routes/platform.routes';
import { errorMiddleware } from './middleware/error.middleware';
import { PriceController } from './controllers/price.controller';
import { PriceIntegrationService } from './integrations/price.service';
import { createDefaultPriceProviders } from './integrations/providers';
import { QuotationService } from './services/quotation.service';
import { QuotationController } from './controllers/quotation.controller';
import { ShareService } from './services/share.service';
import { ShareController } from './controllers/share.controller';
import { TestimonialController } from './controllers/testimonial.controller';
import { getAuthSecrets } from './config/auth-config';
import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/user.repository';
import { PasswordResetTokenRepository } from './repositories/password-reset-token.repository';
import { TestimonialRepository } from './repositories/testimonial.repository';
import { RetailerRepository } from './repositories/retailer.repository';
import { PrismaListRepository } from './repositories/prisma/list.repository';
import { PrismaQuotationRepository } from './repositories/prisma/quotation.repository';
import { PrismaCatalogRepository } from './repositories/prisma/catalog.repository';
import { CatalogController } from './controllers/catalog.controller';
import { readFileSync } from 'node:fs';

export const prisma = new PrismaClient();

/**
 * Monta a aplicação Express sem abrir porta, para que os testes de rota possam
 * exercitar a stack completa (middlewares, validação, controllers, services).
 */
export function createApp(): Express {
  // Falha na inicialização, e não na primeira requisição, se os segredos de
  // assinatura estiverem ausentes ou inseguros.
  getAuthSecrets();

  const app = express();

  // Security middleware
  app.use(helmet());
  app.use(
    cors({
      origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
      credentials: true,
    })
  );

  // Body parsing middleware
  app.use(express.json());
  app.use(cookieParser());

  // Testes permanecem herméticos; execução normal usa PostgreSQL via Prisma.
  const useMemory = process.env.NODE_ENV === 'test' || Boolean(process.env.VITEST);
  const userRepository = useMemory ? new MemoryUserRepository() : new UserRepository(prisma);
  const tokenRepository = useMemory
    ? new MemoryPasswordResetTokenRepository()
    : new PasswordResetTokenRepository(prisma);
  const testimonialRepository = useMemory
    ? new MemoryTestimonialRepository()
    : new TestimonialRepository(prisma);
  const retailerRepository = useMemory
    ? new MemoryRetailerRepository()
    : new RetailerRepository(prisma);
  const listRepository = useMemory ? new MemoryListRepository() : new PrismaListRepository(prisma);
  const quotationRepository = useMemory
    ? new MemoryQuotationRepository()
    : new PrismaQuotationRepository(prisma);
  const catalogRepository = useMemory
    ? new MemoryCatalogRepository()
    : new PrismaCatalogRepository(prisma);

  // Initialize services
  const authService = new AuthService(userRepository, tokenRepository);
  const listService = new ListService(listRepository);
  const priceService = new PriceIntegrationService(createDefaultPriceProviders());
  const quotationService = new QuotationService(
    priceService,
    listRepository,
    quotationRepository,
    catalogRepository
  );
  const shareService = new ShareService(listRepository);

  // Initialize controllers
  const authController = new AuthController(authService);
  const publicController = new PublicController(testimonialRepository, retailerRepository);
  const listController = new ListController(listService);
  const priceController = new PriceController(priceService);
  const quotationController = new QuotationController(quotationService);
  const shareController = new ShareController(shareService);
  const testimonialController = new TestimonialController(testimonialRepository);
  const catalogController = new CatalogController(catalogRepository);

  // Routes
  app.use('/api/auth', createAuthRoutes(authController));
  app.use('/api/public', createPublicRoutes(publicController, shareController));
  app.use(
    '/api/platform',
    createPlatformRoutes(
      authController,
      listController,
      priceController,
      quotationController,
      shareController,
      testimonialController,
      catalogController
    )
  );

  // Health check
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok' });
  });

  app.get('/openapi.yaml', (_req, res, next) => {
    try {
      res
        .type('application/yaml')
        .send(readFileSync(new URL('../openapi.yaml', import.meta.url), 'utf8'));
    } catch (error) {
      next(error);
    }
  });
  app.get('/docs', (_req, res) =>
    res
      .type('html')
      .send(
        `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>COBECO API</title><link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"></head><body><div id="swagger-ui"></div><script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script><script>SwaggerUIBundle({url:'/openapi.yaml',dom_id:'#swagger-ui'});</script></body></html>`
      )
  );

  // Error handling
  app.use(errorMiddleware);

  return app;
}
