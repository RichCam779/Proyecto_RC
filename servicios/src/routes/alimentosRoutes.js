const express = require('express');
const router = express.Router();
const controller = require('../controllers/alimentosController');

router.get('/', controller.getalimentos);
router.get('/:id', controller.getalimentosById);
router.post('/', controller.createalimentos);
router.put('/:id', controller.updatealimentos);
router.delete('/:id', controller.deletealimentos);

module.exports = router;
