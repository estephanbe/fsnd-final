import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ISeller } from 'src/app/interfaces/seller';
import { SingleSellerService } from './single-seller.service';

@Component({
  selector: 'app-single-seller',
  templateUrl: './single-seller.component.html',
  styleUrls: ['./single-seller.component.sass']
})
export class SingleSellerComponent implements OnInit {

  seller: ISeller[] = [];
  errorMessage = '';

  constructor(private router: Router, private route: ActivatedRoute, private sellerService: SingleSellerService) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');

    this.sellerService.getSeller(id).subscribe({
      next: sellerResponse => {
        this.seller = sellerResponse;
      },
      error: err => this.errorMessage = err
    });
  }


}
