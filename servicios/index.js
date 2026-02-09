const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();

// 1. Configuración de CORS
// Vital para que tu API de Python y el navegador se hablen sin pelear
app.use(cors());
app.use(express.json());

// 2. Conexión a Neon PostgreSQL (Blindada)
// Hemos agregado 'connectionTimeoutMillis' para que si la BD duerme, no tire error 502 infinito.
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false // Obligatorio para Neon
  },
  connectionTimeoutMillis: 5000, // Esperar máximo 5s antes de cancelar (Evita cuelgues)
  max: 4 // Máximo de conexiones simultáneas (Ideal para plan gratuito)
});

// 3. Endpoint Principal: Obtener Ubicaciones
app.get('/api/ubicaciones', async (req, res) => {
  try {
    // Tu consulta original filtrando por estado Activo
    const queryText = `
      SELECT id_loc, pais, departamento, ciudad 
      FROM ubicaciones 
      WHERE estado = 'Activo' 
      ORDER BY pais ASC, ciudad ASC
    `;

    // Usamos pool.query directamente (es más simple y seguro para este caso)
    const { rows } = await pool.query(queryText);

    // Tu respuesta con el conteo (Perfecto para el profesor)
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

// 4. Endpoint de Salud
app.get('/', (req, res) => {
  res.send('Servicio de Ubicaciones Externo - NutriScan Pro funcionando ');
});

// 5. Arranque del Servidor (CRUCIAL PARA EVITAR ERROR 502)
// Vercel a veces necesita que el servidor escuche explícitamente en un puerto.
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor de Ubicaciones corriendo en puerto ${PORT}`);
});

// 6. Exportar para Vercel (Compatibilidad Legacy)
module.exports = app;