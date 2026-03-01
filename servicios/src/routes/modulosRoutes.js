const express = require('express');
const router = express.Router();
const controller = require('../controllers/modulosController');

router.get('/', controller.getmodulos);
router.get('/:id', controller.getmodulosById);
router.post('/', controller.createmodulos);
router.put('/:id', controller.updatemodulos);
router.delete('/:id', controller.deletemodulos);

module.exports = router;
