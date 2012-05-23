var express = require('express');

var server = express.createServer();

server.set('view options', {
	layout: false
});

server.set('view engine', 'ejs');
server.set('views', __dirname + "/views");
server.use("/static", express.static(__dirname + "/static"));

server.get("/", function (req, res) {
	res.render("index");
});

server.listen(80)
console.log("Express server started");