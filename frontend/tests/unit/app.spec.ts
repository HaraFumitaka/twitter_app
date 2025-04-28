import { TestBed } from '@angular/core/testing';

describe('基本テスト', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('テストが実行できること', () => {
    expect(true).toBeTruthy();
  });
  
  it('数値の加算が正しく動作すること', () => {
    expect(1 + 1).toBe(2);
  });
});
