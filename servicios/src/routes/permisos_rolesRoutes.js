const express = require('express');
const router = express.Router();
const controller = require('../controllers/permisos_rolesController');

router.get('/', controller.getpermisos_roles);
router.get('/:id', controller.getpermisos_rolesById);
router.post('/', controller.createpermisos_roles);
router.put('/:id', controller.updatepermisos_roles);
router.delete('/:id', controller.deletepermisos_roles);

module.exports = router;
