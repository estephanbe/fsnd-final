import { TestBed } from '@angular/core/testing';

import { SingleSellerService } from './single-seller.service';

describe('SingleSellerService', () => {
  let service: SingleSellerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SingleSellerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
