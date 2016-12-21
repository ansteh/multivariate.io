app.directive('jsonReplicator', function(Socket, $http, $location){
  return {
    restrict: 'E',
    templateUrl: 'static/json-replicator/index.tpl.html',
    scope: {},
    controller: function($scope) {
      $scope.jsonStr = JSON.stringify([{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      },{
        "address": {
          "streetAddress": "21 2nd Street",
          "city": "New York"
        },
        "phoneNumber": [
          {
            "location": "home",
            "code": 44
          }
        ]
      }]);

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
        console.log($scope.json);
        $http.post(encodeURL, {
          input: $scope.json
        })
        .then(function(response) {
          console.log(response);
          return response.data;
        })
        .then(function(data) {
          return $http.post('/replicate/data', data);
        })
        .then(function(response) {
          console.log(response);
        }, function(err) {
          console.log(err);
        })
      }

    }
  };
});
