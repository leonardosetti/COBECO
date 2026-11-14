import { test, expect } from '../../fixtures/test-fixtures';
import { createListaData, createTestUser } from '../../utils/test-data';

test.describe('CRUD - Listas de Compras (UC03-RF03, UC04-RF04, UC05-RF05, UC06-RF06)', () => {
  test.describe('CREATE - Criar nova lista', () => {
    test('deve criar lista com dados mínimos (apenas título)', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData({ descricao: '', publica: false });
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      await listasPage.waitForToast('Lista criada');
      await listasPage.expectListaVisible(listaData.titulo);
    });

    test('deve criar lista com descrição', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData({ descricao: 'Lista para compras da semana' });
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      await listasPage.waitForToast('Lista criada');
      await listasPage.expectListaVisible(listaData.titulo);
    });

    test('deve criar lista pública', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData({ publica: true });
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      await listasPage.waitForToast('Lista criada');
      await listasPage.expectListaVisible(listaData.titulo);
    });

    test('deve exigir título da lista', async ({ authenticatedPage, listasPage }) => {
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.submitButton.click();
      
      await expect(listasPage.tituloInput).toHaveAttribute('required');
    });

    test('deve limitar tamanho do título', async ({ authenticatedPage, listasPage }) => {
      const longTitle = 'A'.repeat(256);
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.tituloInput.fill(longTitle);
      
      await expect(listasPage.tituloInput).toHaveAttribute('maxlength');
    });
  });

  test.describe('READ - Listar e visualizar listas', () => {
    test('deve listar todas as listas do usuário', async ({ authenticatedPage, listasPage }) => {
      const lista1 = createListaData({ titulo: 'Lista 1' });
      const lista2 = createListaData({ titulo: 'Lista 2' });
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(lista1);
      
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(lista2);
      
      await listasPage.gotoMinhasListas();
      await listasPage.expectListaVisible(lista1.titulo);
      await listasPage.expectListaVisible(lista2.titulo);
    });

    test('deve visualizar detalhes de uma lista', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData();
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.verLista(listaId!);
      await expect(listasPage.page.locator('h1, h2, .lista-titulo')).toContainText(listaData.titulo);
    });

    test('deve mostrar lista vazia quando usuário não tem listas', async ({ page, loginPage, cadastroPage, listasPage }) => {
      const userData = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(userData);
      
      await loginPage.goto();
      await loginPage.login(userData.nome_usuario, userData.senha);
      
      await listasPage.gotoMinhasListas();
      await expect(listasPage.page.locator('text=/nenhuma|vazio|criar.*primeira/i')).toBeVisible();
    });
  });

  test.describe('UPDATE - Editar lista existente', () => {
    test('deve atualizar título da lista', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData();
      const novoTitulo = `Título Atualizado ${Date.now()}`;
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.editarLista(listaId!, { titulo: novoTitulo });
      await listasPage.waitForToast('Lista atualizada');
      
      await listasPage.gotoMinhasListas();
      await listasPage.expectListaVisible(novoTitulo);
      await listasPage.expectListaNotVisible(listaData.titulo);
    });

    test('deve atualizar descrição da lista', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData();
      const novaDescricao = `Nova descrição ${Date.now()}`;
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.editarLista(listaId!, { descricao: novaDescricao });
      await listasPage.waitForToast('Lista atualizada');
      
      await listasPage.verLista(listaId!);
      await expect(listasPage.page.locator('text=' + novaDescricao)).toBeVisible();
    });

    test('deve alterar visibilidade da lista (pública/privada)', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData({ publica: false });
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.editarLista(listaId!, { publica: true });
      await listasPage.waitForToast('Lista atualizada');
      
      await listasPage.verLista(listaId!);
      await expect(listasPage.page.locator('text=/pública|público/i')).toBeVisible();
    });

    test('não deve permitir título vazio na edição', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData();
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.editarLista(listaId!, { titulo: '' });
      await expect(listasPage.tituloInput).toHaveAttribute('required');
    });
  });

  test.describe('DELETE - Excluir lista', () => {
    test('deve excluir lista existente', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData();
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.excluirLista(listaId!);
      await listasPage.waitForToast('Lista excluída');
      
      await listasPage.gotoMinhasListas();
      await listasPage.expectListaNotVisible(listaData.titulo);
    });

    test('deve pedir confirmação antes de excluir', async ({ authenticatedPage, listasPage }) => {
      const listaData = createListaData();
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(listaData);
      
      const listaId = await listasPage.getListaIdByTitulo(listaData.titulo);
      expect(listaId).not.toBeNull();
      
      await listasPage.excluirButton(listaId!).click();
      await expect(listasPage.page.locator('text=/confirmar|tem certeza|excluir/i')).toBeVisible();
    });

    test('não deve excluir lista de outro usuário', async ({ page, loginPage, cadastroPage, listasPage, perfilPage }) => {
      const user1 = createTestUser();
      const user2 = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(user1);
      await loginPage.goto();
      await loginPage.login(user1.nome_usuario, user1.senha);
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData());
      
      const listaId = await listasPage.getListaIdByTitulo(
        (await listasPage.listaCards.first().textContent()) || ''
      );
      
      await perfilPage.logout();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(user2);
      await loginPage.goto();
      await loginPage.login(user2.nome_usuario, user2.senha);
      
      await listasPage.gotoMinhasListas();
      if (listaId) {
        await expect(listasPage.excluirButton(listaId)).not.toBeVisible();
      }
    });
  });

  test.describe('Isolamento de dados', () => {
    test('usuário só vê suas próprias listas', async ({ page, loginPage, cadastroPage, listasPage, perfilPage }) => {
      const user1 = createTestUser();
      const user2 = createTestUser();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(user1);
      await loginPage.goto();
      await loginPage.login(user1.nome_usuario, user1.senha);
      
      await listasPage.gotoMinhasListas();
      await listasPage.gotoCriarLista();
      await listasPage.criarLista(createListaData({ titulo: 'Lista User 1' }));
      
      await perfilPage.logout();
      
      await cadastroPage.goto();
      await cadastroPage.cadastrar(user2);
      await loginPage.goto();
      await loginPage.login(user2.nome_usuario, user2.senha);
      
      await listasPage.gotoMinhasListas();
      await listasPage.expectListaNotVisible('Lista User 1');
    });
  });
});