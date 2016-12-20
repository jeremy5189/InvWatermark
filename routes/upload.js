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

    var status = true;

    base_photo.mv(base_photo_new, function(err) {
        if (err) {
            status = false;
            res.status(500).send(err);
        }
        else {
       		console.info('base_photo ok');

            watermark_photo.mv(watermark_photo_new, function(err) {
                if (err) {
                    status = false;
                    res.status(500).send(err);
                }
                else {
                    console.info('watermark_photo ok');

                    if(status) {

                        console.info('Call Shell Encode');

                        shell( '/usr/bin/python', [
                            '/home/jeremy/BlindWaterMark/bwm.py',
                            'encode',
                            base_photo_new,
                            watermark_photo_new,
                            '/home/jeremy/InvWatermark/public/photo/encoded_' + ts + '.png'
                        ], function(ret) {
                            console.log(ret);
                            res.render('encode', {
                                ts: ts
                            });
                        });
                    }
                }
            });
        }
    });


});

router.post('/decode', function(req, res) {

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

    var status = true;

    base_photo.mv(base_photo_new, function(err) {
        if (err) {
            status = false;
            res.status(500).send(err);
        }
        else {
            console.info('base_photo ok');

            watermark_photo.mv(watermark_photo_new, function(err) {
                if (err) {
                    status = false;
                    res.status(500).send(err);
                }
                else {
                    console.info('watermark_photo ok');

                    if(status) {

                        console.info('Call Shell Decode');

                        shell( '/usr/bin/python', [
                            '/home/jeremy/BlindWaterMark/bwm.py',
                            'decode',
                            base_photo_new,
                            watermark_photo_new,
                            '/home/jeremy/InvWatermark/public/photo/decoded_' + ts + '.png'
                        ], function(ret) {
                            console.log(ret);
                            res.render('decode', {
                                ts: ts
                            });
                        });
                    }
                }
            });
        }
    });


});

function shell (cmd, args, callback ) {

	var spawn = require('child_process').spawn;
    var child = spawn(cmd, args);
    var resp = "";

    child.stdout.on('data', function (buffer) { 
        resp += buffer.toString() 
    });

    child.stdout.on('end', function() { 
        callback (resp) 
    });
} 

module.exports = router;
