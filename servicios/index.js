require('dotenv').config();
const express = require('express');
const cors = require('cors');

// Importar rutas de la arquitectura limpia
const routes = require('./src/routes');

const app = express();

// 1. Configuración de CORS
app.use(cors());
app.use(express.json());

// 2. Rutas (Conectado a CRUD controllers)
app.use('/api', routes);

// 3. (Removido: Endpoint Token de prueba local - Autenticación manejada por NutriScan)

// Endpoint raíz
app.get('/', (req, res) => {
  res.send('Servicio de NutriScan Pro funcionando como API Externa con Arquitectura Limpia');
});

// Inicializar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor API corriendo en puerto ${PORT}`);
});

module.exports = app;