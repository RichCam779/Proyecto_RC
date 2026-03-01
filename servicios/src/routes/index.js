const express = require('express');
const router = express.Router();

const rolesRoutes = require('./rolesRoutes');
const modulosRoutes = require('./modulosRoutes');
const usuariosRoutes = require('./usuariosRoutes');
const telefonoRoutes = require('./telefonoRoutes');
const perfiles_clinicosRoutes = require('./perfiles_clinicosRoutes');
const alimentosRoutes = require('./alimentosRoutes');
const permisos_rolesRoutes = require('./permisos_rolesRoutes');
const registro_consumoRoutes = require('./registro_consumoRoutes');
const historialRoutes = require('./historialRoutes');
const historial_chatRoutes = require('./historial_chatRoutes');

router.use('/roles', rolesRoutes);
router.use('/modulos', modulosRoutes);
router.use('/usuarios', usuariosRoutes);
router.use('/telefono', telefonoRoutes);
router.use('/perfiles_clinicos', perfiles_clinicosRoutes);
router.use('/alimentos', alimentosRoutes);
router.use('/permisos_roles', permisos_rolesRoutes);
router.use('/registro_consumo', registro_consumoRoutes);
router.use('/historial', historialRoutes);
router.use('/historial_chat', historial_chatRoutes);

module.exports = router;
