const pool = require('../config/db');

// Obtener todos
const getmodulos = async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM modulos');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Obtener por ID
const getmodulosById = async (req, res) => {
  try {
    const { id } = req.params;
    const { rows } = await pool.query('SELECT * FROM modulos WHERE id_modulo = $1', [id]);
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Crear
const createmodulos = async (req, res) => {
  try {
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    const placeholders = keys.map((_, i) => '$' + (i + 1)).join(', ');
    
    const query = `INSERT INTO modulos (${keys.join(', ')}) VALUES (${placeholders}) RETURNING *`;
    const { rows } = await pool.query(query, values);
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Actualizar
const updatemodulos = async (req, res) => {
  try {
    const { id } = req.params;
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    
    // Si la tabla no envía 'actualizar', forzamos la actualización de la fecha (si la DB no lo hace por Trigger, Express lo asegura)
    if (!keys.includes('actualizar') && !keys.includes('created_at')) {
        // Si hay triggers en DB, esto es redundante pero seguro.
    }

    const setClause = keys.map((key, i) => `${key} = $${i + 1}`).join(', ');
    const query = `UPDATE modulos SET ${setClause} WHERE id_modulo = $${keys.length + 1} RETURNING *`;
    
    values.append(id);
    const { rows } = await pool.query(query, values);
    
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Eliminar / Cambiar estado a Inactivo
const deletemodulos = async (req, res) => {
  try {
    const { id } = req.params;
    let query = `UPDATE modulos SET estado = 'Inactivo' WHERE id_modulo = $1 RETURNING *`;
    
    try {
      const { rows } = await pool.query(query, [id]);
      if (rows.length === 0) {
        query = `DELETE FROM modulos WHERE id_modulo = $1 RETURNING *`;
        const fallback = await pool.query(query, [id]);
        if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
        return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
      }
      res.json({ message: 'Desactivado correctamente', data: rows[0] });
    } catch (e) {
      query = `DELETE FROM modulos WHERE id_modulo = $1 RETURNING *`;
      const fallback = await pool.query(query, [id]);
      if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
      return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = {
  getmodulos,
  getmodulosById,
  createmodulos,
  updatemodulos,
  deletemodulos
};
