export interface IProductSingle {
    id: number;
    name: string;
    description: string;
    creationDate: string;
    updateDate: string;
    price: number;
    numOfSales: number;
    totalSales: number;
    rating: number;
    imageUrl: string;
    cat: object;
    reviews: Array<object>;
    tags: Array<object>;
    seller: object;
}