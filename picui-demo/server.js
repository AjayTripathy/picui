var express = require('express');
var request = require('request');
var socketio = require('socket.io');

var server = express.createServer();

var clients = {}

var io = socketio.listen(server);
io.set('log level', 1);

server.use(express.bodyParser());

server.set('view options', {
	layout: false
});

server.set('view engine', 'ejs');
server.set('views', __dirname + "/views");
server.use("/static", express.static(__dirname + "/static"));

//pointer to the piqui-core server
var coreServer = 'http://www.google.com'; 

server.get("/", function (req, res) {
	res.render("index");
});

server.post("/add", function (req, res) {
	console.log("Adding file");
	var url = req.body.url;
	var id = req.body.id;
	//relay to picui-core and then send back the body, which will be OK or something
	request.post({
		uri: coreServer+"/add",
		body: JSON.stringify({'url' : url, 'treeName' : id})
	}, function (error, response, body) {
		console.log("sent woo");
		res.send(body);
	});
});

server.post("/match", function (req, res) {
	console.log("Matching color(s)");
	var colors = req.body.colors;
	var id = req.body.id;
	var depth = req.body.depth;
	console.log(colors);
	//relay this to piqui-core, send back a list of images
	request.post({
		uri: coreServer+"/match",
		body: JSON.stringify({'colors' : colors, 'limit' : depth, 'treeName' : id })
	}, function (error, response, body) {
		console.log("sent");
		res.send(body);
	});
});

io.sockets.on('connection', function (socket) {
	console.log("Someone has joined");
	clients[socket.id] = socket;
	socket.emit('id', socket.id);

	socket.on('disconnect', function () {
		console.log("Someone has left");
		delete clients[socket.id]
	});
});

server.listen(80);
console.log("Express server started");