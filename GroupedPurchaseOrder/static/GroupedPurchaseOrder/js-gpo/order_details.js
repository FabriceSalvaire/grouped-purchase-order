angular.module('order_details', ['ui.bootstrap']);

angular.module('order_details').controller('ModalController',
					   function ($scope, $modal, $http, $log) {

  $scope.open_update = function (description, quantity, xhr_url, redirect_url) {

    var modalInstance = $modal.open({
      templateUrl: 'UpdateModalContent.html',
      controller: 'UpdateModalInstanceController',
      size: '',
      resolve: {
	description: function () {return description},
	quantity: function () {return quantity}
      }
    });

    modalInstance.result.then(
      function (quantity) {
	$log.info('Modal accepted ' + quantity);
	// XHR
	// $http.post(xhr_url, {quantity: quantity}).
	//   success(function(data, status, headers, config) {
	//     // similar behavior as clicking on a link
	//     window.location.href = redirect_url;
	//   }).error(function(data, status, headers, config) {
	//     alert(data);
	//   });
	ajaxPost(xhr_url, {'quantity': quantity}, function(content)
	   {
	     window.location.href = redirect_url;
	   });
      },
      function () {
	$log.info('Modal dismissed');
      });
  };

  $scope.open_delete = function (description, delete_url) {

    var modalInstance = $modal.open({
      templateUrl: 'DeleteModalContent.html',
      controller: 'DeleteModalInstanceController',
      size: '',
      resolve: {
	description: function () {return description},
      }
    });

    modalInstance.result.then(
      function () {
	$log.info('Modal accepted');
	// $http.get(delete_url); // Ajax
	// similar behavior as clicking on a link
	window.location.href = delete_url;
      },
      function () {
	$log.info('Modal dismissed');
      });
  };
});

angular.module('order_details').controller('UpdateModalInstanceController',
					   function ($scope, $modalInstance, $log, description, quantity) {

  $scope.description = description
  $scope.quantity = quantity;

  $scope.ok = function () {
    var quantity = $("input#id_quantity").val();
    // $log.info('Value ' + quantity);
    $modalInstance.close(quantity);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

angular.module('order_details').controller('DeleteModalInstanceController',
					   function ($scope, $modalInstance, description) {

  $scope.description = description

  $scope.ok = function () {
    $modalInstance.close();
  };
					     
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

// End
