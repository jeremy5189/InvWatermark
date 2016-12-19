var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.post('/encode', function(req, res) {

    var base_photo, watermark_photo, ret;

    if (!req.files) {
        res.send('No files were uploaded.');
        return;
    }

    var ts = new Date().getTime();

    base_photo = req.files.base_photo;
    watermark_photo = req.files.watermark_photo;

    console.info(base_photo);
    console.info(watermark_photo);

    var base_photo_new = '/tmp/base_photo_' + ts + '.png',
    	watermark_photo_new = '/tmp/watermark_photo_' + ts + '.png';

    base_photo.mv(base_photo_new, function(err) {
        if (err) {
            res.status(500).send(err);
        }
        else {
       		console.info('base_photo ok');
        }
    });

    watermark_photo.mv(watermark_photo_new, function(err) {
        if (err) {
            res.status(500).send(err);
        }
        else {
        	console.info('watermark_photo ok');
        }
    });

    res.send('<img src="file:///private/' + base_photo_new + '" alt=""><img src="file:///private/' + watermark_photo_new + '" alt="">');
});

module.exports = router;
