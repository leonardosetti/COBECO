// COBECO Frontend — Formatters & Utils Unit Tests
// Testes para formatCurrency, formatDate, escapeHtml, showToast, showConfirm

import { formatCurrency, formatDate, escapeHtml, showToast, showConfirm } from '../../src/app.js';

describe('Formatters & Utils', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div id="toast-container"></div>
      <div id="modal-container"></div>
    `;
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe('formatCurrency', () => {
    test('formata valor positivo em BRL', () => {
      expect(formatCurrency(1234.56)).toBe('R$ 1.234,56');
    });

    test('formata valor zero', () => {
      expect(formatCurrency(0)).toBe('R$ 0,00');
    });

    test('formata valor com centavos zero', () => {
      expect(formatCurrency(100)).toBe('R$ 100,00');
    });

    test('retorna N/D para null', () => {
      expect(formatCurrency(null)).toBe('N/D');
    });

    test('retorna N/D para undefined', () => {
      expect(formatCurrency(undefined)).toBe('N/D');
    });

    test('formata valores grandes', () => {
      expect(formatCurrency(1234567.89)).toBe('R$ 1.234.567,89');
    });
  });

  describe('formatDate', () => {
    test('formata data ISO para dd/mm/yyyy', () => {
      expect(formatDate('2026-11-14')).toBe('14/11/2026');
    });

    test('formata data com hora', () => {
      expect(formatDate('2026-11-14T10:30:00')).toBe('14/11/2026');
    });

    test('retorna string vazia para null', () => {
      expect(formatDate(null)).toBe('');
    });

    test('retorna string vazia para undefined', () => {
      expect(formatDate(undefined)).toBe('');
    });

    test('retorna string vazia para string vazia', () => {
      expect(formatDate('')).toBe('');
    });
  });

  describe('escapeHtml', () => {
    test('escapa caracteres especiais', () => {
      expect(escapeHtml('<script>alert(1)</script>')).toBe('<script>alert(1)</script>');
    });

    test('escapa aspas', () => {
      expect(escapeHtml('"teste"')).toBe('"teste"');
    });

    test('escapa &', () => {
      expect(escapeHtml('A & B')).toBe('A & B');
    });

    test('retorna string vazia para null', () => {
      expect(escapeHtml(null)).toBe('');
    });

    test('retorna string vazia para undefined', () => {
      expect(escapeHtml(undefined)).toBe('');
    });

    test('não altera texto seguro', () => {
      expect(escapeHtml('Texto normal')).toBe('Texto normal');
    });
  });

  describe('showToast', () => {
    test('cria toast no container', () => {
      showToast('Mensagem de teste', 'success');
      
      const container = document.getElementById('toast-container');
      const toast = container.querySelector('.toast');
      
      expect(toast).toBeTruthy();
      expect(toast.textContent).toContain('Mensagem de teste');
      expect(toast.classList.contains('toast-success')).toBe(true);
      expect(toast.getAttribute('role')).toBe('alert');
    });

    test('toast tem botão de fechar', () => {
      showToast('Teste', 'info');
      
      const toast = document.querySelector('.toast');
      const btn = toast.querySelector('button');
      
      expect(btn).toBeTruthy();
      expect(btn.getAttribute('aria-label')).toBe('Fechar');
    });

    test('clicar no botão remove toast', () => {
      showToast('Teste', 'info');
      
      const btn = document.querySelector('.toast button');
      btn.click();
      
      expect(document.querySelector('.toast')).toBeNull();
    });

    test('auto-remove após 5 segundos', () => {
      showToast('Teste', 'info');
      
      expect(document.querySelector('.toast')).toBeTruthy();
      
      jest.advanceTimersByTime(5000);
      
      expect(document.querySelector('.toast')).toBeNull();
    });

    test('tipos de toast aplicam classes corretas', () => {
      showToast('Success', 'success');
      expect(document.querySelector('.toast').classList.contains('toast-success')).toBe(true);
      
      document.getElementById('toast-container').innerHTML = '';
      showToast('Error', 'error');
      expect(document.querySelector('.toast').classList.contains('toast-error')).toBe(true);
      
      document.getElementById('toast-container').innerHTML = '';
      showToast('Warning', 'warning');
      expect(document.querySelector('.toast').classList.contains('toast-warning')).toBe(true);
    });
  });

  describe('showConfirm', () => {
    test('cria modal com mensagem', () => {
      const promise = showConfirm('Confirma ação?');
      
      const modal = document.querySelector('.modal');
      expect(modal).toBeTruthy();
      expect(modal.querySelector('.modal-body').textContent).toBe('Confirma ação?');
    });

    test('modal tem botão confirmar e cancelar', () => {
      showConfirm('Teste');
      
      const confirmBtn = document.querySelector('[data-action="confirm"]');
      const cancelBtn = document.querySelector('[data-action="cancel"]');
      
      expect(confirmBtn).toBeTruthy();
      expect(cancelBtn).toBeTruthy();
    });

    test('clicar confirmar resolve promise com true', async () => {
      const promise = showConfirm('Teste');
      
      document.querySelector('[data-action="confirm"]').click();
      
      await expect(promise).resolves.toBe(true);
    });

    test('clicar cancelar resolve promise com false', async () => {
      const promise = showConfirm('Teste');
      
      document.querySelector('[data-action="cancel"]').click();
      
      await expect(promise).resolves.toBe(false);
    });

    test('clicar overlay fecha modal com false', async () => {
      const promise = showConfirm('Teste');
      
      document.querySelector('[data-close-overlay]').click();
      
      await expect(promise).resolves.toBe(false);
    });

    test('tecla Escape fecha modal com false', async () => {
      const promise = showConfirm('Teste');
      
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
      
      await expect(promise).resolves.toBe(false);
    });

    test('opções personalizadas: título, textos, classes', () => {
      showConfirm('Mensagem', {
        title: 'Título Custom',
        confirmText: 'Sim',
        cancelText: 'Não',
        confirmClass: 'btn-danger',
        danger: true,
      });
      
      const modal = document.querySelector('.modal');
      expect(modal.querySelector('#modal-title').textContent).toBe('Título Custom');
      expect(modal.querySelector('[data-action="confirm"]').textContent).toBe('Sim');
      expect(modal.querySelector('[data-action="cancel"]').textContent).toBe('Não');
      expect(modal.querySelector('[data-action="confirm"]').classList.contains('btn-danger')).toBe(true);
    });
  });
});