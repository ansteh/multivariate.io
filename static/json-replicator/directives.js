app.directive('jsonReplicator', function(Socket, $http, $location){
  return {
    restrict: 'E',
    templateUrl: 'static/json-replicator/index.tpl.html',
    scope: {},
    controller: function($scope) {
      $scope.jsonStr = JSON.stringify(_.map(_.range(300, 400), function(index){
        return { y: index, x: index+_.random(1000) };
      }));

      var rootLocation = $location.protocol()+"://"+$location.host()+":"+$location.port();

      $scope.updateJSON = function() {
        try {
          $scope.json = JSON.parse($scope.jsonStr);
          if(_.isArray($scope.json) === false) $scope.json = [$scope.json];
        } catch(err) {
          $scope.json = undefined;
        }
      }
      $scope.updateJSON();

      $scope.replicate = function() {
        var encodeURL = $location.protocol()+"://"+$location.host()+":2001/encode/replicate";
        var decodeURL = $location.protocol()+"://"+$location.host()+":2001/decode/replicate";

        $http.post(encodeURL, {
          input: $scope.json
        })
        .then(function(response) {
          return $http.post('/replicate/data', response.data);
        })
        .then(function(response) {
          return $http.post(decodeURL, {
            input: response.data
          });
        })
        .then(function(response) {
          $scope.result = response.data;
        }, function(err) {
          console.log(err);
        })
      }

    }
  };
});
