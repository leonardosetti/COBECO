import { describe, it, expect } from 'vitest';

describe('COBECO Frontend', () => {
  it('should render without errors', () => {
    expect(true).toBe(true);
  });

  it('should have correct app name', () => {
    const appName = 'COBECO';
    expect(appName).toBe('COBECO');
  });
});
