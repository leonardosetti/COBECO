import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export interface ListaData {
  titulo: string;
  descricao?: string;
  publica?: boolean;
}

export interface ItemData {
  nome: string;
  quantidade?: number;
  preco?: number;
  loja?: string;
  url?: string;
  observacao?: string;
}

export class ListasPage extends BasePage {
  readonly criarListaButton: Locator;
  readonly listaNomeInput: Locator;
  readonly salvarListaButton: Locator;
  readonly salvarEdicaoButton: Locator;
  readonly cancelarEdicaoButton: Locator;
  readonly listaRows: Locator;
  readonly listaNomeCell: (nome: string) => Locator;
  readonly editarButton: (listaId: string) => Locator;
  readonly excluirButton: (listaId: string) => Locator;
  readonly verListaLink: (listaId: string) => Locator;
  readonly emptyStateText: Locator;

  // Item management (within criar/editar lista)
  readonly itemProdutoInput: Locator;
  readonly itemQuantidadeInput: Locator;
  readonly addItemButton: Locator;
  readonly itensTableBody: Locator;
  readonly salvarListaFinalButton: Locator;

  constructor(page: Page) {
    super(page);
    this.criarListaButton = page.locator('[data-link="/criar-lista"], a[href="#/criar-lista"]');
    this.listaNomeInput = page.locator('#lista-nome');
    this.salvarListaButton = page.locator('#btn-salvar-lista');
    this.salvarEdicaoButton = page.locator('#btn-salvar-edicao');
    this.cancelarEdicaoButton = page.locator('#btn-cancelar-edicao');
    this.listaRows = page.locator('table tbody tr');
    this.listaNomeCell = (nome: string) => page.locator(`table tbody tr:has-text("${nome}")`);
    this.editarButton = (listaId: string) => page.locator(`button[data-id="${listaId}"], .btn-editar:has-text("Editar")`);
    this.excluirButton = (listaId: string) => page.locator(`.btn-excluir[data-id="${listaId}"], button:has-text("🗑"):near(:text("${listaId}"))`);
    this.verListaLink = (listaId: string) => page.locator(`a[href="#/lista/${listaId}"], a[href="#/lista/${listaId}"]`);
    this.emptyStateText = page.locator('text=/nenhuma lista|criar.*primeira|nenhum item/i');

    // Item management
    this.itemProdutoInput = page.locator('#item-produto');
    this.itemQuantidadeInput = page.locator('#item-quantidade');
    this.addItemButton = page.locator('#btn-add-item');
    this.itensTableBody = page.locator('#tbody-itens');
    this.salvarListaFinalButton = page.locator('#btn-salvar-lista, #btn-salvar-edicao');
  }

  async gotoMinhasListas(): Promise<void> {
    await super.goto('/#/minhas-listas');
    await this.page.waitForLoadState('networkidle');
  }

  async gotoCriarLista(): Promise<void> {
    await this.criarListaButton.click();
    await this.page.waitForLoadState('networkidle');
    await this.listaNomeInput.waitFor({ state: 'visible', timeout: 10000 });
  }

  async criarLista(data: ListaData): Promise<void> {
    await this.listaNomeInput.fill(data.titulo);
    await this.salvarListaButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async editarLista(listaId: string, data: Partial<ListaData>): Promise<void> {
    // Find and click edit button for this list
    const row = this.listaNomeCell(await this.getListaNomeById(listaId));
    await row.locator('button[data-id="editar"], .btn-editar, button:has-text("Editar")').click();
    await this.page.waitForLoadState('networkidle');
    await this.listaNomeInput.waitFor({ state: 'visible', timeout: 10000 });
    
    if (data.titulo !== undefined) await this.listaNomeInput.fill(data.titulo);
    await this.salvarEdicaoButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async excluirLista(listaId: string): Promise<void> {
    const row = this.listaNomeCell(await this.getListaNomeById(listaId));
    const deleteBtn = row.locator('.btn-excluir, button:has-text("🗑")');
    await deleteBtn.click();
    
    // Handle confirmation dialog
    const confirmButton = this.page.locator('button:has-text("Confirmar"), button:has-text("Sim"), button:has-text("Excluir")');
    await confirmButton.waitFor({ state: 'visible', timeout: 5000 });
    await confirmButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async verLista(listaId: string): Promise<void> {
    await this.page.goto(`${this.baseURL}/#/lista/${listaId}`);
    await this.page.waitForLoadState('networkidle');
  }

  async getListaNomeById(listaId: string): Promise<string> {
    // This is a helper - in practice we'd need to track the name
    // For now, return empty string and use other methods
    return '';
  }

  async expectListaVisible(titulo: string): Promise<void> {
    await this.expectVisible(this.listaNomeCell(titulo));
  }

  async expectListaNotVisible(titulo: string): Promise<void> {
    await expect(this.listaNomeCell(titulo)).not.toBeVisible();
  }

  async getListaIdByTitulo(titulo: string): Promise<string | null> {
    const row = this.listaNomeCell(titulo);
    if (await row.isVisible({ timeout: 3000 })) {
      const editBtn = row.locator('button[data-id], .btn-editar, button:has-text("Editar")').first();
      const dataId = await editBtn.getAttribute('data-id');
      if (dataId) return dataId;
      
      const deleteBtn = row.locator('.btn-excluir, button:has-text("🗑")').first();
      return await deleteBtn.getAttribute('data-id');
    }
    return null;
  }

  // Item management methods
  async adicionarItem(produto: string, quantidade: number = 1): Promise<void> {
    await this.itemProdutoInput.fill(produto);
    await this.itemQuantidadeInput.fill(quantidade.toString());
    await this.addItemButton.waitFor({ state: 'visible', timeout: 5000 });
    await this.addItemButton.click();
    await this.page.waitForTimeout(500); // Wait for table update
  }

  async removerItem(produto: string): Promise<void> {
    const row = this.itensTableBody.locator(`tr:has-text("${produto}")`);
    const deleteBtn = row.locator('button:has-text("Remover"), button:has-text("🗑"), .btn-remover');
    await deleteBtn.click();
    await this.page.waitForTimeout(500);
  }

  async expectItemVisible(produto: string): Promise<void> {
    await this.expectVisible(this.itensTableBody.locator(`tr:has-text("${produto}")`));
  }

  async expectEmptyState(): Promise<void> {
    await this.expectVisible(this.emptyStateText);
  }
}