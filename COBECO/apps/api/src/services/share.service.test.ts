import { describe, expect, it } from 'vitest';
import { MemoryListRepository } from '../repositories/memory.repository';
import { ShareService } from './share.service';

describe('ShareService', () => {
  it('creates, resolves and revokes a private list share', async () => {
    const repository = new MemoryListRepository();
    const list = await repository.create('user-1', 'Compras');
    await repository.createItems('user-1', list.id, [{ description: 'Arroz', quantity: 2 }]);
    const service = new ShareService(repository);
    const share = await service.create('user-1', list.id);

    await expect(service.getSharedList(share.token)).resolves.toMatchObject({ name: 'Compras', items: [{ description: 'Arroz' }] });
    await service.revoke('user-1', list.id);
    await expect(service.getSharedList(share.token)).rejects.toMatchObject({ code: 'SHARED_LIST_NOT_FOUND' });
  });

  it('does not expose a list through another user identity', async () => {
    const repository = new MemoryListRepository();
    const list = await repository.create('owner', 'Privada');
    const service = new ShareService(repository);

    await expect(service.create('other', list.id)).rejects.toMatchObject({ code: 'LIST_NOT_FOUND' });
  });
});
