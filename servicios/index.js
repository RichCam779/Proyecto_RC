require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();

// 1. Configuración Básica
app.use(cors());
app.use(express.json());

// 2. Enrutador Principal
const routes = require('./src/routes');
app.use('/api', routes);

// 3. Ruta Base de Comprobación
app.get('/', (req, res) => {
  res.send('Servicio de Ubicaciones Externo - NutriScan Pro funcionando CORRECTAMENTE');
});

// 4. Iniciar Servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor de Ubicaciones corriendo en puerto ${PORT}`);
});

module.exports = app;