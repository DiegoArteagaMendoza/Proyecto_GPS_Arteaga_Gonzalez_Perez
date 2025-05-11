import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { NgModule } from '@angular/core';
import { ProductListComponent } from './components/product-list/product-list.component'; 
import { ProductUploadComponent } from './components/product-upload/product-upload.component';
import { API_URL } from '../../app.config';

const authGuard = () => {
  console.log('API_URL en guardia:', API_URL);
  return true;
};

export const routes: Routes = [
  { path: '', component: DashboardComponent, canActivate: [authGuard] }, // Ruta raíz
  { path: 'productos/', component: ProductListComponent, canActivate: [authGuard] }, // Ruta para listar productos
  { path: 'productos/registrar/', component: ProductUploadComponent, canActivate: [authGuard] }, // Ruta para subir productos
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule{}
