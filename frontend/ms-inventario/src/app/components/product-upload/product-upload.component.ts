import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-product-upload',
  imports: [CommonModule, FormsModule],
  templateUrl: './product-upload.component.html',
  styleUrl: './product-upload.component.css'
})
export class ProductUploadComponent {
  producto = {
    imagen: '',
    nombre: '',
    categoria: '',
    precio: 0,
    stock: 0,
  }

  subirProducto() {
    console.log('Producto subido:', this.producto);
    alert('Producto subido: (simulado) ');
  } 
}
