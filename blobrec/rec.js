//setting up JSON file recorder
const args = process.argv;
if(args.length != 3){
	console.log('Wrong usage!');
	process.exit(1);
}

var jsonfile = require('jsonfile');
var fs = require('fs');
var outfile = args[2];

/**
 * Need the Socket.io client library from npm listed in the package.json
 * a) to connect to the live server the address is dev.mirrorworlds.icat.vt.edu
 * b) to test on localhost, set the address below to 127.0.0.1
 */
var socket = require('socket.io-client')('http://dev.mirrorworlds.icat.vt.edu:8888'); 

socket.emit('start', {connectionType: 'LISTENER', reqCameras: [1]}); 

/**
 * If we wanted to listen for specific camera ids we need to populate a reqCameras field with an array of ids
 * Example: (subscribe to cameras 0,1,and 2)
 * socket.emit('start', {connectionType: 'LISTENER', reqCameras: [0,1,2]}); 
 * 
 * You can also only receive the blobs without the global transformation by adding the local: true field to your spec
 */

/**
 * This will inform the user when the connection to the server occurs to help diagnose between
 * being unable to connect and not recieveing the blobs form the server for some reason
 */
socket.on('connect', function () {
    console.log('connected to server!');
    fs.writeFile(outfile, 'connected to server!\n', function(err){
    	if(err) return console.error(err);
    });
});

/**
 * This will alert the user when a network/socket error is encountered and give a detailed error message
 * so that the issue can be addressed
 */
socket.on('error', function (err) {
    console.log('an error occurred on the socket: ' + err);
});

/**
 * Listen for new blobs and log when they are received
 * The newBlob event will be emitted by the server when a blob has been created.
 */
socket.on('newBlob', function (blob) {
    console.log('[N]: ' + JSON.stringify(blob.id) + ' ' + JSON.stringify(blob.boundingBox));
    fs.writeFile(outfile, (new Date()).getTime() + ',' ,{flag:'a'});
    jsonfile.writeFile(outfile, blob, {flag: 'a'}, function(err){
    	if(err) return console.error(err);
    });
});

/**
 * Listen for update blobs. Logging update blobs is turned off by default as update blobs can come in a steady stream
 * so logging them would clutter stdout and lead to a more confusing example.
 * an updateBlob event will be sent when an existing blobs has updated coordinates to notify of those changes.
 */
socket.on('updateBlob', function (blob) {
    console.log('[U]: ' + JSON.stringify(blob.id) + ' ' + JSON.stringify(blob.boundingBox));
    fs.writeFile(outfile, (new Date()).getTime() + ',' ,{flag:'a'});
    jsonfile.writeFile(outfile, blob, {flag: 'a'}, function(err){
    	if(err) return console.error(err);
    });
});

/**
 * Listen for remove blobs and log when they are received.
 * The removeBlob event will be sent when an existing blob is not longer in the world and should be removed.
 */
socket.on('removeBlob', function (blob) {
    console.log('[R]: ' + JSON.stringify(blob.id) + ' ' + JSON.stringify(blob.boundingBox));
    fs.writeFile(outfile, (new Date()).getTime() + ',' ,{flag:'a'});
    jsonfile.writeFile(outfile, blob, {flag: 'a'}, function(err){
    	if(err) return console.error(err);
    });
});
