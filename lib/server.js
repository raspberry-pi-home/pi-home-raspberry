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
  res.status(500).send('Something went wrong!');
}); // eslint-disable-next-line no-console

app.listen(port, function () {
  return console.log("Example app listening at http://localhost:".concat(port));
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uL3NyYy9zZXJ2ZXIudHMiXSwibmFtZXMiOlsiYXBwIiwicG9ydCIsInVzZSIsImV4cHJlc3MiLCJqc29uIiwiZ2V0IiwicmVxIiwicmVzIiwiYm9keSIsImVyciIsIm5leHQiLCJjb25zb2xlIiwiZXJyb3IiLCJzdGFjayIsInN0YXR1cyIsInNlbmQiLCJsaXN0ZW4iLCJsb2ciXSwibWFwcGluZ3MiOiI7O0FBQUE7O0FBQ0E7O0FBQ0E7Ozs7QUFFQSxJQUFNQSxHQUF3QixHQUFHLDBCQUFqQztBQUNBLElBQU1DLElBQVksR0FBRyxJQUFyQjtBQUVBRCxHQUFHLENBQUNFLEdBQUosQ0FBUSx5QkFBUjtBQUNBRixHQUFHLENBQUNFLEdBQUosQ0FBUUMsb0JBQVFDLElBQVIsRUFBUjtBQUNBSixHQUFHLENBQUNFLEdBQUosQ0FBUSx3QkFBTyxRQUFQLENBQVI7QUFFQUYsR0FBRyxDQUFDSyxHQUFKLENBQVEsR0FBUixFQUFhLFVBQUNDLEdBQUQsRUFBTUMsR0FBTixFQUFjO0FBQ3pCQSxFQUFBQSxHQUFHLENBQUNILElBQUosQ0FBUztBQUFFSSxJQUFBQSxJQUFJLEVBQUU7QUFBUixHQUFUO0FBQ0QsQ0FGRDtBQUlBUixHQUFHLENBQUNFLEdBQUosQ0FBUSxVQUFDTyxHQUFELEVBQVVILEdBQVYsRUFBbUJDLEdBQW5CLEVBQTRCRyxJQUE1QixFQUF5QztBQUMvQztBQUNBQyxFQUFBQSxPQUFPLENBQUNDLEtBQVIsQ0FBY0gsR0FBRyxDQUFDSSxLQUFsQjtBQUNBTixFQUFBQSxHQUFHLENBQUNPLE1BQUosQ0FBVyxHQUFYLEVBQWdCQyxJQUFoQixDQUFxQix1QkFBckI7QUFDRCxDQUpELEUsQ0FNQTs7QUFDQWYsR0FBRyxDQUFDZ0IsTUFBSixDQUFXZixJQUFYLEVBQWlCO0FBQUEsU0FBTVUsT0FBTyxDQUFDTSxHQUFSLHFEQUF5RGhCLElBQXpELEVBQU47QUFBQSxDQUFqQiIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBleHByZXNzIGZyb20gJ2V4cHJlc3MnXG5pbXBvcnQgaGVsbWV0IGZyb20gJ2hlbG1ldCdcbmltcG9ydCBtb3JnYW4gZnJvbSAnbW9yZ2FuJ1xuXG5jb25zdCBhcHA6IGV4cHJlc3MuQXBwbGljYXRpb24gPSBleHByZXNzKClcbmNvbnN0IHBvcnQ6IG51bWJlciA9IDMwMDBcblxuYXBwLnVzZShoZWxtZXQoKSlcbmFwcC51c2UoZXhwcmVzcy5qc29uKCkpXG5hcHAudXNlKG1vcmdhbignY29tbW9uJykpXG5cbmFwcC5nZXQoJy8nLCAocmVxLCByZXMpID0+IHtcbiAgcmVzLmpzb24oeyBib2R5OiAnSGVsbG8gV29ybGQhJyB9KVxufSlcblxuYXBwLnVzZSgoZXJyOmFueSwgcmVxOmFueSwgcmVzOmFueSwgbmV4dDphbnkpID0+IHtcbiAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgY29uc29sZS5lcnJvcihlcnIuc3RhY2spXG4gIHJlcy5zdGF0dXMoNTAwKS5zZW5kKCdTb21ldGhpbmcgd2VudCB3cm9uZyEnKVxufSlcblxuLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbmFwcC5saXN0ZW4ocG9ydCwgKCkgPT4gY29uc29sZS5sb2coYEV4YW1wbGUgYXBwIGxpc3RlbmluZyBhdCBodHRwOi8vbG9jYWxob3N0OiR7cG9ydH1gKSlcbiJdfQ==