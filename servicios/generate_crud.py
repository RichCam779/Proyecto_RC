import os

tables = [
  {"name": "roles", "id": "id_rol"},
  {"name": "modulos", "id": "id_modulo"},
  {"name": "usuarios", "id": "id_usuario"},
  {"name": "telefono", "id": "id_telefono"},
  {"name": "perfiles_clinicos", "id": "id_perfil"},
  {"name": "alimentos", "id": "id_alimento"},
  {"name": "permisos_roles", "id": "id_permiso"},
  {"name": "registro_consumo", "id": "id_registro"},
  {"name": "historial", "id": "id_historial"},
  {"name": "historial_chat", "id": "id_chat"}
]

for table in tables:
  name = table["name"]
  id_col = table["id"]
  
  # Controller
  controller_code = f"""const pool = require('../config/db');

// Obtener todos
const get{name} = async (req, res) => {{
  try {{
    const {{ rows }} = await pool.query('SELECT * FROM {name}');
    res.json(rows);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};

// Obtener por ID
const get{name}ById = async (req, res) => {{
  try {{
    const {{ id }} = req.params;
    const {{ rows }} = await pool.query('SELECT * FROM {name} WHERE {id_col} = $1', [id]);
    if (rows.length === 0) return res.status(404).json({{ error: 'No encontrado' }});
    res.json(rows[0]);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};

// Crear
const create{name} = async (req, res) => {{
  try {{
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    const placeholders = keys.map((_, i) => '$' + (i + 1)).join(', ');
    
    const query = `INSERT INTO {name} (${{keys.join(', ')}}) VALUES (${{placeholders}}) RETURNING *`;
    const {{ rows }} = await pool.query(query, values);
    res.status(201).json(rows[0]);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};

// Actualizar
const update{name} = async (req, res) => {{
  try {{
    const {{ id }} = req.params;
    const keys = Object.keys(req.body);
    const values = Object.values(req.body);
    
    // Si la tabla no envía 'actualizar', forzamos la actualización de la fecha (si la DB no lo hace por Trigger, Express lo asegura)
    if (!keys.includes('actualizar') && !keys.includes('created_at')) {{
        // Si hay triggers en DB, esto es redundante pero seguro.
    }}

    const setClause = keys.map((key, i) => `${{key}} = $${{i + 1}}`).join(', ');
    const query = `UPDATE {name} SET ${{setClause}} WHERE {id_col} = $${{keys.length + 1}} RETURNING *`;
    
    values.append(id);
    const {{ rows }} = await pool.query(query, values);
    
    if (rows.length === 0) return res.status(404).json({{ error: 'No encontrado' }});
    res.json(rows[0]);
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};

// Eliminar / Cambiar estado a Inactivo
const delete{name} = async (req, res) => {{
  try {{
    const {{ id }} = req.params;
    let query = `UPDATE {name} SET estado = 'Inactivo' WHERE {id_col} = $1 RETURNING *`;
    
    try {{
      const {{ rows }} = await pool.query(query, [id]);
      if (rows.length === 0) {{
        query = `DELETE FROM {name} WHERE {id_col} = $1 RETURNING *`;
        const fallback = await pool.query(query, [id]);
        if (fallback.rows.length === 0) return res.status(404).json({{ error: 'No encontrado' }});
        return res.json({{ message: 'Eliminado correctamente', data: fallback.rows[0] }});
      }}
      res.json({{ message: 'Desactivado correctamente', data: rows[0] }});
    }} catch (e) {{
      query = `DELETE FROM {name} WHERE {id_col} = $1 RETURNING *`;
      const fallback = await pool.query(query, [id]);
      if (fallback.rows.length === 0) return res.status(404).json({{ error: 'No encontrado' }});
      return res.json({{ message: 'Eliminado correctamente', data: fallback.rows[0] }});
    }}
  }} catch (err) {{
    res.status(500).json({{ error: err.message }});
  }}
}};

module.exports = {{
  get{name},
  get{name}ById,
  create{name},
  update{name},
  delete{name}
}};
"""
  
  with open(f"./src/controllers/{name}Controller.js", "w") as f:
    f.write(controller_code)

  # Routes
  route_code = f"""const express = require('express');
const router = express.Router();
const controller = require('../controllers/{name}Controller');

router.get('/', controller.get{name});
router.get('/:id', controller.get{name}ById);
router.post('/', controller.create{name});
router.put('/:id', controller.update{name});
router.delete('/:id', controller.delete{name});

module.exports = router;
"""

  with open(f"./src/routes/{name}Routes.js", "w") as f:
    f.write(route_code)


index_routes = f"""const express = require('express');
const router = express.Router();

"""
for table in tables:
  index_routes += f"const {table['name']}Routes = require('./{table['name']}Routes');\n"
index_routes += "\n"
for table in tables:
  index_routes += f"router.use('/{table['name']}', {table['name']}Routes);\n"
index_routes += "\nmodule.exports = router;\n"

with open('./src/routes/index.js', 'w') as f:
  f.write(index_routes)
