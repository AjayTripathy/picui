var express = require('express');
var request = require('request');

var server = express.createServer();

server.use(express.bodyParser());

server.set('view options', {
	layout: false
});

server.set('view engine', 'ejs');
server.set('views', __dirname + "/views");
server.use("/static", express.static(__dirname + "/static"));

//pointer to the piqui-core server
var coreServer = 'null'; 

server.get("/", function (req, res) {
	res.render("index");
});

server.post("/add", function (req, res) {
	console.log("Adding file");
	var url = req.body.url;
	console.log(url);
	//relay to picui-core and then send back the body, which will be OK or something
	request.post({
		uri: coreServer+"/add",
		body: JSON.stringify({'url' : url})
	}, function (error, response, body) {
		console.log("sent woo");
		res.send(body); //maybe should be res.send(response)?
	});
});

server.post("/match", function (req, res) {
	console.log("Matching color(s)");
	var colors = req.body.colors;
	console.log(colors);
	//relay this to piqui-core, send back a list of images
	request.post({
		uri: coreServer+"/match",
		body: JSON.stringify({'colors' : colors})
	}, function (error, response, body) {
		console.log("sent");
		res.send(body);
	});
});

server.listen(80)
console.log("Express server started");