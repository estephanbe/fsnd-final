import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-add-product',
  templateUrl: './add-product.component.html',
  styleUrls: ['./add-product.component.sass']
})
export class AddProductComponent implements OnInit {
  productName = '';

  constructor() { }

  ngOnInit(): void {
  }

  getFormValues(values: object): void {
    console.log(values);
  }

}
