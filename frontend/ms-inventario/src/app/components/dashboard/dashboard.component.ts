import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopBarComponent } from '../top-bar/top-bar.component';
import { SideMenuComponent } from '../side-menu/side-menu.component';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, TopBarComponent, SideMenuComponent, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  constructor(private router: Router) {}
  navegar(ruta: string) {
    if (ruta) {
      this.router.navigate([ruta]);
    }
  }

  nombreFarmacia = 'San José'; // Esto se actualizará según quién inicie sesión

  botones = [
    { texto: 'Listar Inventario', icon: 'bx-list-ul', ruta: '/listar-productos' },
    { texto: 'Subir Producto', icon: 'bx-upload', ruta: '/subir-producto' },
    { texto: 'Actualizar Inventario', icon: 'bx-edit' },
    { texto: 'Eliminar Producto', icon: 'bx-trash' }
  ];
}

