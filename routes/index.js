var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index');
});

router.get('/decode', function(req, res, next) {
  res.render('index_decode');
});

module.exports = router;
