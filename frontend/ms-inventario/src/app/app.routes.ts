import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { NgModule } from '@angular/core';
import { ProductListComponent } from './components/product-list/product-list.component'; 


export const routes: Routes = [
  { path: '', component: DashboardComponent }, // Ruta raíz
  { path: 'listar-productos', component: ProductListComponent}, // Ruta para listar productos
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule{}
