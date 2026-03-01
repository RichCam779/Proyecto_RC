const express = require('express');
const router = express.Router();
const controller = require('../controllers/historialController');

router.get('/', controller.gethistorial);
router.get('/:id', controller.gethistorialById);
router.post('/', controller.createhistorial);
router.put('/:id', controller.updatehistorial);
router.delete('/:id', controller.deletehistorial);

module.exports = router;
