const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();

// 1. Configuración de CORS
// Esto permite que tu API de Python o tu Frontend consulten este servicio sin errores de seguridad
app.use(cors());
app.use(express.json());

// 2. Conexión a Neon PostgreSQL
// Usamos la variable de entorno DATABASE_URL que configurarás en Vercel
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false // Requerido para la conexión segura con Neon
  }
});

// 3. Endpoint Principal: Obtener Ubicaciones
// Filtra por estado 'Activo' y ordena alfabéticamente por país y ciudad
app.get('/api/ubicaciones', async (req, res) => {
  try {
    const queryText = `
      SELECT id_loc, pais, departamento, ciudad 
      FROM ubicaciones 
      WHERE estado = 'Activo' 
      ORDER BY pais ASC, ciudad ASC
    `;

    const { rows } = await pool.query(queryText);

    // Respondemos con los datos y un conteo para que el profesor vea el volumen de datos
    res.json({
      total: rows.length,
      data: rows
    });

  } catch (err) {
    console.error('Error en la base de datos:', err);
    res.status(500).json({
      error: 'Error al consultar el servicio de geografía',
      details: err.message
    });
  }
});

// 4. Endpoint de Salud (Para verificar que el servicio está vivo)
app.get('/', (req, res) => {
  res.send('Servicio de Ubicaciones Externo - NutriScan Pro funcionando 🚀');
});

// 5. Exportar para Vercel
module.exports = app;