const pool = require('../config/db');

// Obtener todos
const getpermisos_roles = async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM permisos_roles');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Obtener por ID
const getpermisos_rolesById = async (req, res) => {
  try {
    const { id } = req.params;
    const { rows } = await pool.query('SELECT * FROM permisos_roles WHERE id_permiso = $1', [id]);
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Crear
const createpermisos_roles = async (req, res) => {
  try {
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    const placeholders = keys.map((_, i) => '$' + (i + 1)).join(', ');
    
    const query = `INSERT INTO permisos_roles (${keys.join(', ')}) VALUES (${placeholders}) RETURNING *`;
    const { rows } = await pool.query(query, values);
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Actualizar
const updatepermisos_roles = async (req, res) => {
  try {
    const { id } = req.params;
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    
    // Si la tabla no envía 'actualizar', forzamos la actualización de la fecha (si la DB no lo hace por Trigger, Express lo asegura)
    if (!keys.includes('actualizar') && !keys.includes('created_at')) {
        // Si hay triggers en DB, esto es redundante pero seguro.
    }

    const setClause = keys.map((key, i) => `${key} = $${i + 1}`).join(', ');
    const query = `UPDATE permisos_roles SET ${setClause} WHERE id_permiso = $${keys.length + 1} RETURNING *`;
    
    values.append(id);
    const { rows } = await pool.query(query, values);
    
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Eliminar / Cambiar estado a Inactivo
const deletepermisos_roles = async (req, res) => {
  try {
    const { id } = req.params;
    let query = `UPDATE permisos_roles SET estado = 'Inactivo' WHERE id_permiso = $1 RETURNING *`;
    
    try {
      const { rows } = await pool.query(query, [id]);
      if (rows.length === 0) {
        query = `DELETE FROM permisos_roles WHERE id_permiso = $1 RETURNING *`;
        const fallback = await pool.query(query, [id]);
        if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
        return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
      }
      res.json({ message: 'Desactivado correctamente', data: rows[0] });
    } catch (e) {
      query = `DELETE FROM permisos_roles WHERE id_permiso = $1 RETURNING *`;
      const fallback = await pool.query(query, [id]);
      if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
      return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = {
  getpermisos_roles,
  getpermisos_rolesById,
  createpermisos_roles,
  updatepermisos_roles,
  deletepermisos_roles
};
