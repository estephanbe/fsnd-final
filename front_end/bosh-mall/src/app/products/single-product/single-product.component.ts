import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from './product.service';
import { SellingDialogComponent } from './selling-dialog/selling-dialog.component';

@Component({
  selector: 'app-single-product',
  templateUrl: './single-product.component.html',
  styleUrls: ['./single-product.component.sass']
})
export class SingleProductComponent implements OnInit {
  product = {};
  errorMessage = '';

  constructor(private router: Router, private route: ActivatedRoute, private productService: ProductService, public dialog: MatDialog) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.productService.getProduct(id).subscribe({
      next: productResponse => {
        this.product = productResponse;
      },
      error: err => this.errorMessage = err
    });
  }

  openDialog(id: number): void {
    this.productService.sellProduct(id).subscribe({
      next: productResponse => {
        this.product = productResponse;
      },
      error: err => this.errorMessage = err
    });
    this.dialog.open(SellingDialogComponent);
  }

}


