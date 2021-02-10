import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'convertPrice'
})
export class ConvertPricePipe implements PipeTransform {

  transform(value: number): number {
    return Math.round(value);
  }

}
