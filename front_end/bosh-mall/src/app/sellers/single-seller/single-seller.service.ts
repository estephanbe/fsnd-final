import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { ISeller } from 'src/app/interfaces/seller';


@Injectable({
  providedIn: 'root'
})
export class SingleSellerService {
  private dataUrl = 'http://127.0.0.1:5000/sellers/';

  constructor(private http: HttpClient) { }

  getSeller(id: any): Observable<ISeller[]> {
    this.dataUrl = 'http://127.0.0.1:5000/sellers/' + id;
    console.log(this.dataUrl);
    return this.http.get<ISeller[]>(this.dataUrl)
      .pipe(
        tap(data => {
          console.log(data);
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
