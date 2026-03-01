const express = require('express');
const router = express.Router();
const controller = require('../controllers/usuariosController');

router.get('/', controller.getusuarios);
router.get('/:id', controller.getusuariosById);
router.post('/', controller.createusuarios);
router.put('/:id', controller.updateusuarios);
router.delete('/:id', controller.deleteusuarios);

module.exports = router;
