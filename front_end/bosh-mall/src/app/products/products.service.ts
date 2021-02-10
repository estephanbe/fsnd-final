import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { IProducts } from '../interfaces/products';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  private dataUrl = '';

  constructor(private http: HttpClient) { }

  getProducts(page: number, sorting: string, catID: number, tagID: number): Observable<IProducts[]> {
    console.log(catID);
    if (catID){
      this.dataUrl = 'http://127.0.0.1:5000/categories/' + catID + '/products?page=' + page;
    } else if (tagID){
      this.dataUrl = 'http://127.0.0.1:5000/tags/' + tagID + '/products?page=' + page;
    } else {
      this.dataUrl = 'http://127.0.0.1:5000/products?page=' + page;
    }

    if (sorting){
      this.dataUrl += '&sort=' + sorting;
    }

    return this.http.get<IProducts[]>(this.dataUrl)
      .pipe(
        tap(data => {
          // console.log(data);
        }),
        catchError(this.handleError)
      );
  }

  private handleError(err: HttpErrorResponse) {
    // in a real world app, we may send the server to some remote logging infrastructure
    // instead of just logging it to the console
    let errorMessage = '';
    if (err.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      errorMessage = `An error occurred: ${err.error.message}`;
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      errorMessage = `Server returned code: ${err.status}, error message is: ${err.message}`;
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }



}
