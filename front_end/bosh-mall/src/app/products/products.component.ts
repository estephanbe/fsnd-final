import { Component, OnInit } from '@angular/core';
import { IProduct } from '../interfaces/product';
import { IProducts } from '../interfaces/products';
import { ProductsService } from './products.service';


@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.sass']
})
export class ProductsComponent implements OnInit {
  title = 'Store Products';
  apiResponse: IProducts[] = [];

  products: IProduct[] = [];
  totalProducts = 0;
  productsSum = 0;
  noMoreProducts = false;
  noLastProducts = true;
  page = 1;
  catID = 0;
  tagID = 0;
  sorting = 'dateO';

  _sortingOption = 'dateO';
  get sortingOption(): string {
    return this._sortingOption;
  }
  set sortingOption(value: string) {
    this.sorting = value;
    this.getProducts();
  }

  _categoriesOption = 'dateO';
  get categoriesOption(): string {
    return this._categoriesOption;
  }
  set categoriesOption(value: string) {
    this.catID = parseInt(value, 0);
    this.getProducts();
  }

  errorMessage = '';

  tagSelect(value: number): void {
    this.tagID = value;
    this.getProducts();
  }

  resetProductsFromTags(): void {
    this.tagID = 0;
    this.getProducts();
  }

  constructor(private productsService: ProductsService) { }

  ngOnInit(): void {
    this.getProducts();
  }

  nextProducts(): void {
    this.productsSum += this.products.length;
    console.log(this.totalProducts, this.productsSum);
    if (this.totalProducts !== this.productsSum) {
      console.log('more');
      this.page++;
      this.getProducts();
      this.noLastProducts = false;
    } else {
      this.noMoreProducts = true;
    }
  }

  lastProducts(): void {
    console.log(this.totalProducts, this.productsSum, this.noLastProducts);
    if (this.productsSum > 0) {
      this.productsSum -= this.products.length;
      this.page--;
      this.getProducts();
    } else {
      this.noLastProducts = true;
    }
  }

  getProducts(): void {
    this.productsService.getProducts(this.page, this.sorting, this.catID, this.tagID).subscribe({
      next: productsResponse => {
        this.apiResponse = productsResponse;
        this.products = productsResponse.products;
        this.totalProducts = this.apiResponse.total_products;

        console.log(this.apiResponse);

        // this.apiResponse = productsResponse;
        // console.log(this.apiResponse.products)
        // this.products = productsResponse.products;
      },
      error: err => this.errorMessage = err
    });
  }
}
