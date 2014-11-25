// (function() {
// "use strict";
// })();

var application = angular.module('crud_orders', ['ngCookies', 'ngResource', 'ng.django.forms']);

application.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

application.run(function($http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});

application.factory('Order', ['$resource', function($resource) {
    return $resource('/crud/orders/', {'pk': '@pk'}, {
    });
}]);

// application.controller('order_controller', function ($scope) {
//   $scope.orders = [
//     {'duty_tax': '0',},
//   ];
// });

application.controller('order_controller', ['$scope', 'Order', function ($scope, Order) {
    // Query returns an array of objects, Order.objects.all() by default
    $scope.orders = Order.query();
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
