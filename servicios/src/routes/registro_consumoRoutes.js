const express = require('express');
const router = express.Router();
const controller = require('../controllers/registro_consumoController');

router.get('/', controller.getregistro_consumo);
router.get('/:id', controller.getregistro_consumoById);
router.post('/', controller.createregistro_consumo);
router.put('/:id', controller.updateregistro_consumo);
router.delete('/:id', controller.deleteregistro_consumo);

module.exports = router;
