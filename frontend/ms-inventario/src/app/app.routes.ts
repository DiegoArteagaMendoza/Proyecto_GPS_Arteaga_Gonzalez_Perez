import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { NgModule } from '@angular/core';
import { ProductListComponent } from './components/product-list/product-list.component'; 
import { ProductUploadComponent } from './components/product-upload/product-upload.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent }, // Ruta raíz
  { path: 'listar-productos', component: ProductListComponent }, // Ruta para listar productos
  {path: 'subir-producto', component: ProductUploadComponent}, // Ruta para subir productos
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule{}
