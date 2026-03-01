const express = require('express');
const router = express.Router();
const controller = require('../controllers/perfiles_clinicosController');

router.get('/', controller.getperfiles_clinicos);
router.get('/:id', controller.getperfiles_clinicosById);
router.post('/', controller.createperfiles_clinicos);
router.put('/:id', controller.updateperfiles_clinicos);
router.delete('/:id', controller.deleteperfiles_clinicos);

module.exports = router;
