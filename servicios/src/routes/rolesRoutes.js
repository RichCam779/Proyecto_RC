const express = require('express');
const router = express.Router();
const controller = require('../controllers/rolesController');

router.get('/', controller.getroles);
router.get('/:id', controller.getrolesById);
router.post('/', controller.createroles);
router.put('/:id', controller.updateroles);
router.delete('/:id', controller.deleteroles);

module.exports = router;
