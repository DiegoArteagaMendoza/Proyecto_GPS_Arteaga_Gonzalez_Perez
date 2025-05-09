import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // necesario para *ngFor

interface Producto {
  id: number;
  nombre: string;
  laboratorio: string;
  lote: string;
  bodega: string;
  tipoVenta: string;
  fechaVencimiento: string;
  precio: number;
  stock: number;
  imagen: string;
}

@Component({
  selector: 'app-product-list',
  standalone: true, // importante
  imports: [CommonModule], // MUY IMPORTANTE para que funcione *ngFor
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {
  productos: Producto[] = [];

  ngOnInit(): void {
    this.productos = [
      {
        id: 1,
        nombre: 'Paracetamol',
        laboratorio: 'Lab A',
        lote: 'L123',
        bodega: 'Bodega Central',
        tipoVenta: 'Libre',
        fechaVencimiento: '2025-12-31',
        precio: 1500,
        stock: 30,
        imagen: 'imagen paracetamol'
      },
      {
        id: 2,
        nombre: 'Ibuprofeno',
        laboratorio: 'Lab B',
        lote: 'L456',
        bodega: 'Bodega Norte',
        tipoVenta: 'Receta',
        fechaVencimiento: '2026-03-15',
        precio: 2500,
        stock: 45,
        imagen: 'imagen ibuprofeno'
      }
    ];
  }
}
