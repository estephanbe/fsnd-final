import { Component, OnInit } from '@angular/core';
import { ISellers } from '../interfaces/sellers';
import { SellersService } from './sellers.service';

@Component({
  selector: 'app-sellers',
  templateUrl: './sellers.component.html',
  styleUrls: ['./sellers.component.sass']
})
export class SellersComponent implements OnInit {

  apiResponse: ISellers[] = [];
  sellers = [];
  totalSellers = 0;

  errorMessage = '';


  constructor(private sellersService: SellersService) { }

  ngOnInit(): void {
    this.getSellers();
  }

  getSellers(): void {
    this.sellersService.getSellers().subscribe({
      next: sellersResponse => {
        this.apiResponse = sellersResponse;
        this.sellers = sellersResponse.sellers;
        this.totalSellers = sellersResponse.total_sellers;

        console.log(this.sellers, this.totalSellers);

      },
      error: err => this.errorMessage = err
    });
  }

}
