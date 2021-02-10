import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AddProductComponent } from './products/add-product/add-product/add-product.component';
import { ProductsComponent } from './products/products.component';
import { SingleProductComponent } from './products/single-product/single-product.component';
import { SellersComponent } from './sellers/sellers.component';
import { SingleSellerComponent } from './sellers/single-seller/single-seller.component';
import { WelcomeComponent } from './welcome/welcome/welcome.component';

const routes: Routes = [
  {path: 'add_product', component: AddProductComponent},
  {path: 'products/:id', component: SingleProductComponent},
  {path: 'products', component: ProductsComponent},
  {path: 'sellers/:id', component: SingleSellerComponent},
  {path: 'sellers', component: SellersComponent},
  { path: 'welcome', component: WelcomeComponent },
  { path: '', redirectTo: 'welcome', pathMatch: 'full' },
  { path: '**', redirectTo: 'welcome', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
