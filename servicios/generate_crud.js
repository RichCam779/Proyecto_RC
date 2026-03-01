const fs = require('fs');

const tables = [
  { name: 'roles', id: 'id_rol' },
  { name: 'modulos', id: 'id_modulo' },
  { name: 'usuarios', id: 'id_usuario' },
  { name: 'telefono', id: 'id_telefono' },
  { name: 'perfiles_clinicos', id: 'id_perfil' },
  { name: 'alimentos', id: 'id_alimento' },
  { name: 'permisos_roles', id: 'id_permiso' },
  { name: 'registro_consumo', id: 'id_registro' },
  { name: 'historial', id: 'id_historial' },
  { name: 'historial_chat', id: 'id_chat' }
];

tables.forEach(table => {
  // Controller
  const controllerCode = `const pool = require('../config/db');

// Obtener todos
const get${table.name} = async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM ${table.name}');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Obtener por ID
const get${table.name}ById = async (req, res) => {
  try {
    const { id } = req.params;
    const { rows } = await pool.query('SELECT * FROM ${table.name} WHERE ${table.id} = $1', [id]);
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Crear
const create${table.name} = async (req, res) => {
  try {
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    const placeholders = keys.map((_, i) => '$' + (i + 1)).join(', ');
    
    const query = \\\`INSERT INTO ${table.name} (\\\${keys.join(', ')}) VALUES (\\\${placeholders}) RETURNING *\\\`;
    const { rows } = await pool.query(query, values);
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Actualizar
const update${table.name} = async (req, res) => {
  try {
    const { id } = req.params;
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    
    const setClause = keys.map((key, i) => \\\`\\\${key} = $\\\${i + 1}\\\`).join(', ');
    const query = \\\`UPDATE ${table.name} SET \\\${setClause} WHERE ${table.id} = $\\\${keys.length + 1} RETURNING *\\\`;
    
    values.push(id);
    const { rows } = await pool.query(query, values);
    
    if (rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Eliminar / Cambiar estado a Inactivo
const delete${table.name} = async (req, res) => {
  try {
    const { id } = req.params;
    let query = \\\`UPDATE ${table.name} SET estado = 'Inactivo' WHERE ${table.id} = $1 RETURNING *\\\`;
    
    const { rows } = await pool.query(query, [id]);
    
    if (rows.length === 0) {
      // Intentar borrado físico si no tiene columna estado
      query = \\\`DELETE FROM ${table.name} WHERE ${table.id} = $1 RETURNING *\\\`;
      const fallback = await pool.query(query, [id]);
      if (fallback.rows.length === 0) return res.status(404).json({ error: 'No encontrado' });
      return res.json({ message: 'Eliminado correctamente', data: fallback.rows[0] });
    }
    res.json({ message: 'Desactivado correctamente', data: rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = {
  get${table.name},
  get${table.name}ById,
  create${table.name},
  update${table.name},
  delete${table.name}
};
`;

  fs.writeFileSync(`./src/controllers/${table.name}Controller.js`, controllerCode);

  // Routes
  const routeCode = `const express = require('express');
const router = express.Router();
const controller = require('../controllers/${table.name}Controller');
const { authenticateJWT } = require('../middlewares/authMiddleware');

router.get('/', authenticateJWT, controller.get${table.name});
router.get('/:id', authenticateJWT, controller.get${table.name}ById);
router.post('/', authenticateJWT, controller.create${table.name});
router.put('/:id', authenticateJWT, controller.update${table.name});
router.delete('/:id', authenticateJWT, controller.delete${table.name});

module.exports = router;
`;

  fs.writeFileSync(`./src/routes/${table.name}Routes.js`, routeCode);
});

// Index builder for routes
const indexRoutes = `const express = require('express');
const router = express.Router();

${tables.map(t => `const ${t.name}Routes = require('./${t.name}Routes');`).join('\n')}

${tables.map(t => `router.use('/${t.name}', ${t.name}Routes);`).join('\n')}

module.exports = router;
`;
fs.writeFileSync('./src/routes/index.js', indexRoutes);
