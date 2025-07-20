const fs = require('fs-extra');
const path = require('path');

const SECCIONES = [
    'inicio',
    'ms-farmacia',
    'ms-inventario',
    'ms-trabajador',
    'ms-usuariocliente',
    'ms-venta'
];

const DEST = path.join(__dirname, 'dist');

// Limpiar carpeta dist
fs.emptyDirSync(DEST);

SECCIONES.forEach(seccion => {
    const SOURCE_HTML = path.join(__dirname, seccion, 'src', 'html');
    const SOURCE_CSS = path.join(__dirname, seccion, 'src', 'css');
    const SOURCE_JS = path.join(__dirname, seccion, 'src', 'js');
    const DEST_SECCION = path.join(DEST, seccion);

    // Copiar HTML
    fs.copySync(SOURCE_HTML, DEST_SECCION);

    // Copiar CSS
    const DEST_CSS = path.join(DEST_SECCION, 'css');
    fs.copySync(SOURCE_CSS, DEST_CSS);

    // Copiar JS
    const DEST_JS = path.join(DEST_SECCION, 'js');
    fs.copySync(SOURCE_JS, DEST_JS);
});

// Copiar index.html raíz a dist/index.html
const SOURCE_INDEX = path.join(__dirname, 'index.html');
const DEST_INDEX = path.join(DEST, 'index.html');
fs.copySync(SOURCE_INDEX, DEST_INDEX);

console.log('✅ Build completado. Todas las secciones están listas en /dist/');