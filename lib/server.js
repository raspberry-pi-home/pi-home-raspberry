"use strict";

var _express = _interopRequireDefault(require("express"));

var _helmet = _interopRequireDefault(require("helmet"));

var _morgan = _interopRequireDefault(require("morgan"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var app = (0, _express["default"])();
var port = 3000;
app.use((0, _helmet["default"])());
app.use(_express["default"].json());
app.use((0, _morgan["default"])('common'));
app.get('/', function (req, res) {
  res.json({
    body: 'Hello World!'
  });
});
app.use(function (err, req, res, next) {
  // eslint-disable-next-line no-console
  console.error(err.stack);
  res.status(500).send('Something broke!');
}); // eslint-disable-next-line no-console

app.listen(port, function () {
  return console.log("Example app listening at http://localhost:".concat(port));
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uL3NyYy9zZXJ2ZXIudHMiXSwibmFtZXMiOlsiYXBwIiwicG9ydCIsInVzZSIsImV4cHJlc3MiLCJqc29uIiwiZ2V0IiwicmVxIiwicmVzIiwiYm9keSIsImVyciIsIm5leHQiLCJjb25zb2xlIiwiZXJyb3IiLCJzdGFjayIsInN0YXR1cyIsInNlbmQiLCJsaXN0ZW4iLCJsb2ciXSwibWFwcGluZ3MiOiI7O0FBQUE7O0FBQ0E7O0FBQ0E7Ozs7QUFFQSxJQUFNQSxHQUF3QixHQUFHLDBCQUFqQztBQUNBLElBQU1DLElBQVksR0FBRyxJQUFyQjtBQUVBRCxHQUFHLENBQUNFLEdBQUosQ0FBUSx5QkFBUjtBQUNBRixHQUFHLENBQUNFLEdBQUosQ0FBUUMsb0JBQVFDLElBQVIsRUFBUjtBQUNBSixHQUFHLENBQUNFLEdBQUosQ0FBUSx3QkFBTyxRQUFQLENBQVI7QUFFQUYsR0FBRyxDQUFDSyxHQUFKLENBQVEsR0FBUixFQUFhLFVBQUNDLEdBQUQsRUFBTUMsR0FBTixFQUFjO0FBQ3pCQSxFQUFBQSxHQUFHLENBQUNILElBQUosQ0FBUztBQUFFSSxJQUFBQSxJQUFJLEVBQUU7QUFBUixHQUFUO0FBQ0QsQ0FGRDtBQUlBUixHQUFHLENBQUNFLEdBQUosQ0FBUSxVQUFDTyxHQUFELEVBQU1ILEdBQU4sRUFBV0MsR0FBWCxFQUFnQkcsSUFBaEIsRUFBeUI7QUFDL0I7QUFDQUMsRUFBQUEsT0FBTyxDQUFDQyxLQUFSLENBQWNILEdBQUcsQ0FBQ0ksS0FBbEI7QUFDQU4sRUFBQUEsR0FBRyxDQUFDTyxNQUFKLENBQVcsR0FBWCxFQUFnQkMsSUFBaEIsQ0FBcUIsa0JBQXJCO0FBQ0QsQ0FKRCxFLENBTUE7O0FBQ0FmLEdBQUcsQ0FBQ2dCLE1BQUosQ0FBV2YsSUFBWCxFQUFpQjtBQUFBLFNBQU1VLE9BQU8sQ0FBQ00sR0FBUixxREFBeURoQixJQUF6RCxFQUFOO0FBQUEsQ0FBakIiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgZXhwcmVzcyBmcm9tICdleHByZXNzJ1xuaW1wb3J0IGhlbG1ldCBmcm9tICdoZWxtZXQnXG5pbXBvcnQgbW9yZ2FuIGZyb20gJ21vcmdhbic7XG5cbmNvbnN0IGFwcDogZXhwcmVzcy5BcHBsaWNhdGlvbiA9IGV4cHJlc3MoKVxuY29uc3QgcG9ydDogbnVtYmVyID0gMzAwMFxuXG5hcHAudXNlKGhlbG1ldCgpKVxuYXBwLnVzZShleHByZXNzLmpzb24oKSlcbmFwcC51c2UobW9yZ2FuKCdjb21tb24nKSlcblxuYXBwLmdldCgnLycsIChyZXEsIHJlcykgPT4ge1xuICByZXMuanNvbih7IGJvZHk6ICdIZWxsbyBXb3JsZCEnIH0pXG59KVxuXG5hcHAudXNlKChlcnIsIHJlcSwgcmVzLCBuZXh0KSA9PiB7XG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1jb25zb2xlXG4gIGNvbnNvbGUuZXJyb3IoZXJyLnN0YWNrKVxuICByZXMuc3RhdHVzKDUwMCkuc2VuZCgnU29tZXRoaW5nIGJyb2tlIScpXG59KVxuXG4vLyBlc2xpbnQtZGlzYWJsZS1uZXh0LWxpbmUgbm8tY29uc29sZVxuYXBwLmxpc3Rlbihwb3J0LCAoKSA9PiBjb25zb2xlLmxvZyhgRXhhbXBsZSBhcHAgbGlzdGVuaW5nIGF0IGh0dHA6Ly9sb2NhbGhvc3Q6JHtwb3J0fWApKVxuIl19