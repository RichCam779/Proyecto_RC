const express = require('express');
const router = express.Router();
const controller = require('../controllers/telefonoController');

router.get('/', controller.gettelefono);
router.get('/:id', controller.gettelefonoById);
router.post('/', controller.createtelefono);
router.put('/:id', controller.updatetelefono);
router.delete('/:id', controller.deletetelefono);

module.exports = router;
