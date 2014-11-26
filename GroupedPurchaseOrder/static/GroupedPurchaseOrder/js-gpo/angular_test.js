// (function() {
// "use strict";
// })();

var services = angular.module('CrudOrderServices', ['ngResource']);

services.factory('Supplier', ['$resource', function($resource) {
  return $resource('/api/v1/supplier/:pk/?format=json', {'pk': '@pk'}, {
    'query':  {method:'GET', isArray:false},
  });
}]);

services.factory('Order', ['$resource', function($resource) {
  // http://127.0.0.1:8000/crud/orders/
  // http://127.0.0.1:8000/crud/orders/?pk=1
  // return $resource('/crud/orders/', {'pk': '@pk'}, {
  // });
  // http://127.0.0.1:8000/api/v1/order/1/?format=json
  return $resource('/api/v1/order/:pk/?format=json', {'pk': '@pk'}, {
    'query':  {method:'GET', isArray:false},
  });
}]);

var application = angular.module('crud_order', ['ngCookies', 'CrudOrderServices']);

application.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

application.run(function($http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});

// application.controller('order_controller', function ($scope) {
//   $scope.orders = [
//     {'duty_tax': '0',},
//   ];
// });

application.controller('order_controller',
		       ['$scope', '$log', 'Supplier', 'Order',
			function ($scope, $log, Supplier, Order) {
			  // var response = 
			  Order.query(function (response) {
			    var orders = response.objects;
			    $scope.orders = orders;
			    for (var i = 0; i < orders.length; i++) {
			      order = orders[i];
			      var f = function (i) {
				var ii = i;
				return function (supplier) {
     				  $scope.orders[ii].supplier = supplier;
				}};
			      Supplier.get({'pk': order.supplier}, f(i));
			    };
			  });
			}]);

// Getting a single object
// var model = MyModel.get({pk: 1});
// 
// 
// // We can crete new objects
// var new_model = new MyModel({name: 'New name'});
// new_model.$save(function(){
//    $scope.models.push(new_model);
// });
// // In callback we push our new object to the models array
// 
// // Updating objects
// new_model.name = 'Test name';
// new_model.$save();
// 
// // Deleting objects
// new_model.$remove();
// // This deletes the object on server, but it still exists in the models array
// // To delete it in frontend we have to remove it from the models array
