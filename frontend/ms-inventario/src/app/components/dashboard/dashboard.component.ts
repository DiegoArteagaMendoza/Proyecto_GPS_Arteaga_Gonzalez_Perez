import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopBarComponent } from '../top-bar/top-bar.component';
import { SideMenuComponent } from '../side-menu/side-menu.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, TopBarComponent, SideMenuComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  nombreFarmacia = 'San José'; // Esto se actualizará según quién inicie sesión

  botones = [
    { texto: 'Listar Inventario', icon: 'bx-list-ul' },
    { texto: 'Subir Producto', icon: 'bx-upload' },
    { texto: 'Actualizar Inventario', icon: 'bx-edit' },
    { texto: 'Eliminar Producto', icon: 'bx-trash' }
  ];
}
