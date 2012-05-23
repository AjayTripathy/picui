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
var coreServer = ""; 

server.get("/", function (req, res) {
	res.render("index");
});

server.post("/add", function (req, res) {
	console.log("Adding file");
	var url = req.body.url;
	console.log(url);
	//todo: relay this to piqui-core

});

server.post("/match", function (req, res) {
	console.log("Matching color");
	var colors = req.body.colors;
	console.log(colors);
	//tidiL relay this to piqui-core
})

server.listen(80)
console.log("Express server started");