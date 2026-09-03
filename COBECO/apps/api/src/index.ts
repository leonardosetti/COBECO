import 'dotenv/config';
import { createApp, prisma } from './app';

const PORT = process.env.PORT || 3333;

function startServer() {
  const app = createApp();

  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(
      process.env.NODE_ENV === 'test'
        ? 'Persistence: memória de teste'
        : 'Persistence: Prisma/PostgreSQL'
    );
  });
}

try {
  startServer();
} catch (error) {
  console.error('Falha ao iniciar a API:', error instanceof Error ? error.message : error);
  process.exit(1);
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  await prisma.$disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT received, shutting down gracefully');
  await prisma.$disconnect();
  process.exit(0);
});
