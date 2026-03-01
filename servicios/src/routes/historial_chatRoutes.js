const express = require('express');
const router = express.Router();
const controller = require('../controllers/historial_chatController');

router.get('/', controller.gethistorial_chat);
router.get('/:id', controller.gethistorial_chatById);
router.post('/', controller.createhistorial_chat);
router.put('/:id', controller.updatehistorial_chat);
router.delete('/:id', controller.deletehistorial_chat);

module.exports = router;
