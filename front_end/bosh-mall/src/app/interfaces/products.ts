import { IProduct } from './product';

export interface IProducts {
    cats: Array<any>;
    tags: Array<any>;
    products: Array<IProduct>;
    sucess: boolean;
    total_products: number;
}