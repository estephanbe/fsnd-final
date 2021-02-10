import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleSellerComponent } from './single-seller.component';

describe('SingleSellerComponent', () => {
  let component: SingleSellerComponent;
  let fixture: ComponentFixture<SingleSellerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SingleSellerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SingleSellerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
