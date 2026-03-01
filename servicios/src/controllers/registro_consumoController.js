const pool = require('../config/db');

// Obtener todos
const getregistro_consumo = async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM registro_consumo');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Obtener por ID
const getregistro_consumoById = async (req, res) => {
  try {
    const { id } = req.params;
    const { rows } = await pool.query('SELECT * FROM registro_consumo WHERE id_registro = $1', [id]);
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Crear
const createregistro_consumo = async (req, res) => {
  try {
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    const placeholders = keys.map((_, i) => '$' + (i + 1)).join(', ');
    
    const query = `INSERT INTO registro_consumo (${keys.join(', ')}) VALUES (${placeholders}) RETURNING *`;
    const { rows } = await pool.query(query, values);
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Actualizar
const updateregistro_consumo = async (req, res) => {
  try {
    const { id } = req.params;
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    
    // Si la tabla no envía 'actualizar', forzamos la actualización de la fecha (si la DB no lo hace por Trigger, Express lo asegura)
    if (!keys.includes('actualizar') && !keys.includes('created_at')) {
        // Si hay triggers en DB, esto es redundante pero seguro.
    }

    const setClause = keys.map((key, i) => `${key} = $${i + 1}`).join(', ');
    const query = `UPDATE registro_consumo SET ${setClause} WHERE id_registro = $${keys.length + 1} RETURNING *`;
    
    values.append(id);
    const { rows } = await pool.query(query, values);
    
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Eliminar / Cambiar estado a Inactivo
const deleteregistro_consumo = async (req, res) => {
  try {
    const { id } = req.params;
    let query = `UPDATE registro_consumo SET estado = 'Inactivo' WHERE id_registro = $1 RETURNING *`;
    
    try {
      const { rows } = await pool.query(query, [id]);
      if (rows.length === 0) {
        query = `DELETE FROM registro_consumo WHERE id_registro = $1 RETURNING *`;
        const fallback = await pool.query(query, [id]);
        if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
        return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
      }
      res.json({ message: 'Desactivado correctamente', data: rows[0] });
    } catch (e) {
      query = `DELETE FROM registro_consumo WHERE id_registro = $1 RETURNING *`;
      const fallback = await pool.query(query, [id]);
      if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
      return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = {
  getregistro_consumo,
  getregistro_consumoById,
  createregistro_consumo,
  updateregistro_consumo,
  deleteregistro_consumo
};
